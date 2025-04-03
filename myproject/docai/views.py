import os
from django.shortcuts import render
from django.conf import settings
from .forms import PDFForm, QueryForm
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from .models import*
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
import re



embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
vector_store = None
def index(request):
    return render(request, 'index.html')
def load_pdf_and_create_vector_store(file_path):
    global vector_store
    loader = PyPDFLoader(file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    extracted_data = text_splitter.split_documents(data)
    vector_store = FAISS.from_documents(extracted_data, embeddings)
    vector_store.save_local(os.path.join(settings.MEDIA_ROOT, 'doc_ai'))

def clear_previous_pdf_and_vector_store():
    global vector_store
    vector_store = None
    media_root = settings.MEDIA_ROOT
    for file in os.listdir(media_root):
        if file.endswith('.pdf'):
            os.remove(os.path.join(media_root, file))
    vector_store_path = os.path.join(media_root, 'doc_ai')
    if os.path.exists(vector_store_path):
        for file in os.listdir(vector_store_path):
            os.remove(os.path.join(vector_store_path, file))
        os.rmdir(vector_store_path)



def home(request):
    global vector_store
    pdf_form = PDFForm()
    query_form = QueryForm()

    # Clear chat_history on every GET request (page load or reload)
    if request.method == 'GET':
        request.session['chat_history'] = []
        request.session.modified = True  # Ensure the session is marked as modified

    if request.method == 'POST':
        if 'pdf_submit' in request.POST:
            pdf_form = PDFForm(request.POST, request.FILES)
            if pdf_form.is_valid():
                clear_previous_pdf_and_vector_store()
                pdf_instance = pdf_form.save()
                pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_instance.pdf_file.name)
                load_pdf_and_create_vector_store(pdf_path)
                request.session['chat_history'].append({'type': 'message', 'content': 'New PDF uploaded successfully!'})
                request.session.modified = True
                print(os.getcwd())
            else:
                request.session['chat_history'].append({'type': 'error', 'content': 'PDF upload failed. Please upload a valid PDF file.'})
                request.session.modified = True
        elif 'query_submit' in request.POST:
            query_form = QueryForm(request.POST)
            if query_form.is_valid():
                query = query_form.cleaned_data['query']
                model_name = query_form.cleaned_data['model_choice']
                if not query:
                    request.session['chat_history'].append({'type': 'error', 'content': 'Please enter a question to get an answer.'})
                else:
                    request.session['chat_history'].append({'type': 'question', 'content': query})
                    
                    groq_api_key = os.environ.get("GROQ_API_KEY")
                    
                    if not groq_api_key:
                        request.session['chat_history'].append({'type': 'error', 'content': 'GROQ_API_KEY environment variable is not set.'})
                    else:
                        try:
                            llm = ChatGroq(api_key=groq_api_key, model_name=model_name)
                            if vector_store:
                                retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
                                prompt = ChatPromptTemplate.from_template(
                                    """Answer the questions based on the provided context only.
                                    <context>
                                    {context}
                                    </context>
                                    Question: {input}
                                    """
                                )
                                que_chain = create_stuff_documents_chain(llm, prompt)
                                rag_chain = create_retrieval_chain(retriever, que_chain)
                                response = rag_chain.invoke({"input": query})
                                answer1 = response['answer']
                                answer =  re.sub(r"<think>.*?</think>", "",answer1, flags=re.DOTALL).strip()
                               
                            else:
                                prompt = ChatPromptTemplate.from_template("Question: {input}")
                                response = llm.invoke(prompt.format(input=query))
                                answer1 = response.content 
                               
                                answer =  re.sub(r"<think>.*?</think>", "",answer1, flags=re.DOTALL).strip()
                               
                            request.session['chat_history'].append({'type': 'answer', 'content': answer})
                        except Exception as e:
                            request.session['chat_history'].append({'type': 'error', 'content': f'Error processing query: {str(e)}'})
                request.session.modified = True
            else:
                request.session['chat_history'].append({'type': 'error', 'content': 'Invalid query form submission. Please check your input.'})
                request.session.modified = True

    # Debugging: Print the session to verify it's cleared
    # print("Chat history after request handling:", request.session.get('chat_history', []))

    chat_history = request.session.get('chat_history', [])
    return render(request, 'home.html', {
        'pdf_form': pdf_form,
        'query_form': QueryForm(),
        'chat_history': chat_history
    })
def register(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password  = request.POST.get('password')
        
        user = User.objects.filter(username= username)
        if user.exists():
            messages.info(request, 'Username already exists')
            return redirect('/register/')

        user = User.objects.create(
        username = username,
        first_name = first_name,
        last_name = last_name,
        )
        user.set_password(password)
        user.save()
        messages.info(request, 'account ceated succefully')

    return render(request, 'register.html')

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/')
    else:
        return render(request, 'login.html')



