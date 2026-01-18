import os
import google.generativeai as genai
from dotenv import load_dotenv
import pypdf
import nltk
from unidecode import unidecode
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer

# --- CONFIGURAÇÕES INICIAIS ---

# 1. Carrega variáveis de ambiente
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# 2. Configurações do NLTK (Baixa dicionários se não tiver)
def baixar_recursos_nltk():
    recursos = ['punkt', 'stopwords', 'rslp', 'punkt_tab']
    for recurso in recursos:
        try:
            nltk.data.find(f'tokenizers/{recurso}')
        except LookupError:
            try:
                nltk.data.find(f'corpora/{recurso}')
            except LookupError:
                try:
                    nltk.data.find(f'stemmers/{recurso}')
                except LookupError:
                    nltk.download(recurso, quiet=True)

baixar_recursos_nltk()

# --- FUNÇÕES DE ARQUIVO ---

def ler_arquivo(caminho_arquivo):
    """Lê o conteúdo bruto de PDF ou TXT"""
    ext = os.path.splitext(caminho_arquivo)[1].lower()
    texto_completo = ""

    try:
        if ext == '.txt':
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                texto_completo = f.read()
        elif ext == '.pdf':
            reader = pypdf.PdfReader(caminho_arquivo)
            for page in reader.pages:
                texto = page.extract_text()
                if texto: texto_completo += texto + "\n"
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return ""

    return texto_completo

# --- CAMADA 1: PRÉ-PROCESSAMENTO (NLP CLÁSSICO) ---

def realizar_preprocessamento(texto):
    """
    Aplica técnicas de NLP e RETORNA UMA LISTA.
    """
    if not texto: return []

    tokens = word_tokenize(texto.lower(), language='portuguese')
    stop_words = set(stopwords.words('portuguese'))
    stemmer = RSLPStemmer()
    
    tokens_uteis = []
    
    for word in tokens:
        if word.isalnum() and word not in stop_words:
            raiz = stemmer.stem(word)
            raiz = unidecode(raiz)
            tokens_uteis.append(raiz)
            
    # MUDANÇA AQUI: Retorna a LISTA ['palavra', 'palavra'], não a STRING "palavra palavra"
    return tokens_uteis
def classificar_por_regras(tokens_processados):
    """
    Classifica baseando-se na contagem de palavras-chave (stems).
    O uso de SETS {} (Hash Table) torna a busca instantânea.
    """
    
    # CONJUNTO DE PALAVRAS PRODUTIVAS (HASH TABLE)
    stems_produtivos = {
        'err', 'falh', 'suport', 'ajud', 'duvid', 'problem', 'urgent',
        'acess', 'bug', 'solicit', 'precis', 'trav', 'atualiz', 'orcament',
        'cot', 'ped', 'envi', 'nao', 'funcion'
    }
    
    # CONJUNTO DE PALAVRAS IMPRODUTIVAS (HASH TABLE)
    stems_improdutivos = {
        'obrig', 'paraben', 'valeu', 'agradec', 'bom', 'tard', 'noit', 
        'felic', 'excel', 'grati', 'ok', 'cient', 'recebid', 'abrac', 'perfeit'
    }
    
    score_produtivo = 0
    score_improdutivo = 0
    
    # Loop único: Verifica cada token diretamente nas tabelas hash
    for token in tokens_processados:
        if token in stems_produtivos:
            score_produtivo += 1
        elif token in stems_improdutivos:
            score_improdutivo += 1
            
    # Lógica de decisão final
    if score_produtivo > 0:
        return "Produtivo"
    elif score_improdutivo > 0:
        return "Improdutivo"
    else:
        return "Indefinido"

# --- ETAPA 3: IA (GEMINI) ---
# Adicione o parametro tokens_processados aqui
def consultar_gemini(texto_original, tokens_processados_str=""):
    if not api_key: return None

    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Analise o email abaixo.
    
    DADOS:
    - Original: "{texto_original}"
    - Palavras-chave técnicas (Stemming): "{tokens_processados_str}"

    1. Classifique ESTRITAMENTE como "Produtivo" (Requer ação/suporte) ou "Improdutivo" (Agradecimento/Spam).
    2. Gere uma sugestão de resposta.
    Email: "{texto_original}"

    Formato de Saída:
    Categoria: [Produtivo/Improdutivo]
    Motivo: [Explicação curta]
    Resposta Sugerida: [Texto da resposta]
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        
        # Parser simples
        resultado = {"categoria": "Indefinido", "motivo": "", "sugestao_resposta": ""}
        linhas = text.split('\n')
        buffer = []
        capturando = False
        
        for linha in linhas:
            l = linha.strip()
            if l.startswith("Categoria:"):
                resultado["categoria"] = l.replace("Categoria:", "").strip()
            elif l.startswith("Motivo:"):
                resultado["motivo"] = l.replace("Motivo:", "").strip()
            elif l.startswith("Resposta Sugerida:"):
                capturando = True
                c = l.replace("Resposta Sugerida:", "").strip()
                if c: buffer.append(c)
            elif capturando:
                buffer.append(linha)
        
        resultado["sugestao_resposta"] = "\n".join(buffer).strip()
        return resultado
    except:
        return None
   
# --- ETAPA 4: ORQUESTRADOR E COMPARAÇÃO (NOVO) ---
def processar_email_completo(texto_original):
    # 1. Pré-processamento (Agora retorna uma LISTA)
    tokens_lista = realizar_preprocessamento(texto_original)
    
    # 2. Classificação via Regras (Agora funciona, pois recebe uma LISTA)
    classificacao_regras = classificar_por_regras(tokens_lista)
    
    # 3. Classificação via IA
    # OBS: Aqui convertemos a lista em string só para o Gemini ler melhor
    tokens_string_para_ia = " ".join(tokens_lista) 
    
    # Passamos o texto original E a string de tokens para a função da IA
    resultado_ia = consultar_gemini(texto_original, tokens_string_para_ia)
    
    if not resultado_ia:
        return {
            "status": "erro",
            "mensagem": "Não foi possível conectar com a IA."
        }

    classificacao_ia = resultado_ia["categoria"]
    
    # ... (O resto da lógica de comparação continua igual) ...
    
    match_produtivo = ("produtivo" in classificacao_regras.lower() and "produtivo" in classificacao_ia.lower())
    match_improdutivo = ("improdutivo" in classificacao_regras.lower() and "improdutivo" in classificacao_ia.lower())

    if match_produtivo or match_improdutivo:
        return {
            "status": "sucesso",
            "categoria_final": classificacao_ia,
            "motivo": resultado_ia["motivo"],
            "sugestao_resposta": resultado_ia["sugestao_resposta"],
            "debug_regras": classificacao_regras,
            "debug_ia": classificacao_ia
        }
    else:
        return {
            "status": "conflito",
            "mensagem_aviso": "Não foi possível determinar o assunto da mensagem com precisão.",
            "detalhe_conflito": f"Regras dizem '{classificacao_regras}', mas IA diz '{classificacao_ia}'.",
            "sugestao_ia_opcional": resultado_ia["sugestao_resposta"] 
        }