
import json, os

# Cria pastas se nao existirem
os.makedirs('css', exist_ok=True)
os.makedirs('js', exist_ok=True)
os.makedirs('data', exist_ok=True)

# INDEX.HTML
html = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Me Ajuda a Listar</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;background:#f5f5f5;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px;}
#app{width:100%;max-width:480px;margin:0 auto;}
.card{background:#fff;border-radius:16px;box-shadow:0 4px 24px rgba(0,0,0,0.08);padding:32px 24px;text-align:center;}
.card h2{color:#232F3E;font-size:22px;margin-bottom:12px;}
.card p{color:#555;font-size:15px;line-height:1.5;margin-bottom:12px;}
.highlight{color:#FF9900;font-weight:bold;}
.input-field{width:100%;padding:14px;border:2px solid #FF9900;border-radius:10px;font-size:16px;margin:16px 0;outline:none;}
.input-field:focus{border-color:#146EB4;box-shadow:0 0 0 3px rgba(20,110,180,0.1);}
.btn-primary{background:#FF9900;color:#fff;border:none;padding:16px 32px;border-radius:10px;font-size:18px;font-weight:bold;cursor:pointer;width:100%;transition:background 0.2s;}
.btn-primary:hover{background:#e88a00;}
.btn-option{display:block;width:100%;margin:8px 0;padding:16px;background:#fff;border:2px solid #FF9900;border-radius:10px;font-size:16px;cursor:pointer;color:#232F3E;font-weight:500;transition:all 0.2s;text-align:left;}
.btn-option:hover{background:#FF9900;color:#fff;}
.btn-link{display:block;width:100%;margin:8px 0;padding:16px;background:#146EB4;border:none;border-radius:10px;font-size:16px;cursor:pointer;color:#fff;font-weight:500;text-decoration:none;text-align:center;}
.btn-link:hover{background:#0f5a94;}
.info-box{background:#FFF3E0;border-left:4px solid #FF9900;padding:14px;border-radius:8px;text-align:left;margin:14px 0;font-size:14px;color:#333;}
.warning-box{background:#FFEBEE;border-left:4px solid #D32F2F;padding:14px;border-radius:8px;text-align:left;margin:14px 0;font-size:14px;color:#C62828;}
.steps{text-align:left;margin:16px 0;}
.step{background:#f8f9fa;padding:12px 16px;border-radius:8px;margin:6px 0;font-size:14px;color:#333;}
.step strong{color:#FF9900;}
.footer-nav{display:flex;gap:8px;justify-content:center;margin-top:20px;padding-top:16px;border-top:1px solid #eee;flex-wrap:wrap;}
.footer-btn{background:#f0f0f0;border:none;padding:10px 16px;border-radius:8px;font-size:13px;cursor:pointer;color:#555;text-decoration:none;}
.footer-btn:hover{background:#ddd;color:#232F3E;}
.footer-link{background:#146EB4;color:#fff;padding:10px 16px;border-radius:8px;font-size:13px;text-decoration:none;}
.error-msg{color:#D32F2F;font-size:13px;display:none;margin-top:4px;}
.logo{font-size:28px;color:#FF9900;font-weight:bold;margin-bottom:8px;}
</style>
</head>
<body>
<div id="app"><div class="card"><p>Carregando...</p></div></div>
<script src="js/app.js"></script>
</body>
</html>'''

# APP.JS
appjs = '''var SHEETDB_URL = "https://sheetdb.io/api/v1/7x95jmwaouxrl";
var flowData = {};
var historico = [];
var contato = "";

function init() {
  fetch("data/flow.json")
    .then(function(r) { return r.json(); })
    .then(function(d) { flowData = d; pedirContato(); })
    .catch(function() {
      document.getElementById("app").innerHTML = "<div class=\\"card\\"><h2>Erro</h2><p>Nao foi possivel carregar. Recarregue a pagina.</p></div>";
    });
}

function pedirContato() {
  var h = "<div class=\\"card\\">";
  h += "<div class=\\"logo\\">Me Ajuda a Listar</div>";
  h += "<h2>Ola! Vou te ajudar a listar seu produto na Amazon</h2>";
  h += "<p>Primeiro, me deixe um dado de contato para te ajudarmos se precisar.</p>";
  h += "<p class=\\"highlight\\">100% gratuito!</p>";
  h += "<input id=\\"contato\\" class=\\"input-field\\" type=\\"text\\" placeholder=\\"WhatsApp com DDD ou Nome da Loja\\" />";
  h += "<p id=\\"erro\\" class=\\"error-msg\\">Por favor, digite seu WhatsApp ou Nome da Loja para continuar</p>";
  h += "<button class=\\"btn-primary\\" onclick=\\"comecar()\\">Comecar!</button>";
  h += "</div>";
  document.getElementById("app").innerHTML = h;
}

function comecar() {
  var v = document.getElementById("contato").value.trim();
  if (!v) { document.getElementById("erro").style.display = "block"; return; }
  contato = v;
  try {
    fetch(SHEETDB_URL, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({data: {whatsapp: v, observacao: "inicio", tela: "inicio"}})
    });
  } catch(e) {}
  mostrarTela("inicio");
}

function mostrarTela(id) {
  var s = flowData[id];
  if (!s) { document.getElementById("app").innerHTML = "<div class=\\"card\\"><h2>Ops!</h2><p>Tela nao encontrada. Volte ao inicio.</p></div>"; return; }
  historico.push(id);

  var h = "<div class=\\"card\\">";
  h += "<h2>" + s.question + "</h2>";

  if (s.info) { h += "<div class=\\"info-box\\">" + s.info + "</div>"; }
  if (s.warning) { h += "<div class=\\"warning-box\\">" + s.warning + "</div>"; }

  if (s.steps) {
    h += "<div class=\\"steps\\">";
    for (var i = 0; i < s.steps.length; i++) {
      h += "<div class=\\"step\\"><strong>" + (i+1) + ".</strong> " + s.steps[i] + "</div>";
    }
    h += "</div>";
  }

  if (s.options) {
    for (var j = 0; j < s.options.length; j++) {
      var o = s.options[j];
      if (o.link) {
        h += "<a class=\\"btn-link\\" href=\\"" + o.link + "\\" target=\\"_blank\\">" + o.text + "</a>";
      } else {
        h += "<button class=\\"btn-option\\" onclick=\\"mostrarTela(\\'" + o.next + "\\')\\">" + o.text + "</button>";
      }
    }
  }

  if (historico.length > 1) {
    h += "<div class=\\"footer-nav\\">";
    h += "<button class=\\"footer-btn\\" onclick=\\"voltar()\\">Voltar</button>";
    h += "<button class=\\"footer-btn\\" onclick=\\"mostrarTela(\\'inicio\\')\\">Inicio</button>";
    h += "<a class=\\"footer-link\\" href=\\"https://amazonexteu.qualtrics.com/jfe/form/SV_eEhccc2rqm5WURw\\" target=\\"_blank\\">Lista pra mim</a>";
    h += "</div>";
  }

  h += "</div>";
  document.getElementById("app").innerHTML = h;
}

function voltar() {
  historico.pop();
  var anterior = historico.pop();
  if (anterior) { mostrarTela(anterior); }
  else { pedirContato(); }
}

init();'''

# FLOW.JSON - Arvore completa 1 a 1 com SOPs
flow = {
  "inicio": {
    "question": "Vamos listar seu produto!",
    "info": "Vou te guiar passo a passo, como se estivesse ao seu lado.",
    "options": [
      {"text": "Meu produto e NOVO", "next": "tem_ean"},
      {"text": "Meu produto e USADO / Seminovo", "next": "usado"}
    ]
  },
  "tem_ean": {
    "question": "Seu produto tem codigo de barras (EAN)?",
    "info": "EAN e aquele codigo de barras numerico na embalagem do produto (comeca com 789 ou 790 no Brasil).",
    "options": [
      {"text": "Sim, tenho EAN", "next": "validar_ean"},
      {"text": "Nao tenho EAN", "next": "marca_pergunta"}
    ]
  },
  "validar_ean": {
    "question": "Valide seu EAN antes de continuar",
    "steps": [
      "Acesse o site do GS1 clicando no botao abaixo",
      "Digite seu EAN na barra de busca",
      "Se aparecer os dados do produto = EAN valido",
      "Se nao encontrar = EAN pode estar incorreto"
    ],
    "options": [
      {"text": "Validar meu EAN no GS1", "link": "https://www.gs1.org/services/verified-by-gs1/results"},
      {"text": "EAN validado! Proximo passo", "next": "ean_marca"},
      {"text": "EAN nao encontrado/invalido", "next": "ean_invalido"}
    ]
  },
  "ean_invalido": {
    "question": "EAN nao encontrado?",
    "info": "Pode ser que o fabricante ainda nao cadastrou no GS1 ou o numero esta errado.",
    "options": [
      {"text": "Vou conferir o numero e tentar de novo", "next": "validar_ean"},
      {"text": "Quero listar sem EAN (como generico)", "next": "sop_generico"},
      {"text": "Preciso de ajuda", "next": "ajuda_final"}
    ]
  },
  "ean_marca": {
    "question": "Seu produto tem marca na embalagem?",
    "info": "Impresso, gravado ou estampado no produto. Adesivo ou costurado NAO conta.",
    "options": [
      {"text": "Sim, tem marca", "next": "marca_sua_ou_terceiro"},
      {"text": "Nao tem marca (generico)", "next": "sop_com_ean_generico"}
    ]
  },
  "marca_sua_ou_terceiro": {
    "question": "A marca e sua ou voce revende?",
    "options": [
      {"text": "Marca propria (eu sou o dono)", "next": "marca_propria_inpi"},
      {"text": "Revendo (marca de terceiro)", "next": "revendedor_nf"}
    ]
  },
  "marca_propria_inpi": {
    "question": "Voce tem registro no INPI?",
    "info": "INPI = Instituto Nacional da Propriedade Industrial. E o orgao que registra marcas no Brasil.",
    "options": [
      {"text": "Sim, tenho INPI aprovado", "next": "brand_registry"},
      {"text": "INPI em andamento (processo aberto)", "next": "brand_registry"},
      {"text": "Nao tenho INPI", "next": "sem_inpi_logo"}
    ]
  },
  "brand_registry": {
    "question": "Registre sua marca na Amazon (Brand Registry)",
    "steps": [
      "Acesse o link abaixo para o Brand Registry",
      "Faca o cadastro com seu numero do INPI",
      "Aguarde aprovacao (pode levar alguns dias)",
      "Apos aprovado, voce lista com todos os beneficios de marca"
    ],
    "info": "Com Brand Registry voce tem: paginas A+, protecao contra copias, e mais controle sobre suas listagens.",
    "options": [
      {"text": "Ir para o Brand Registry", "link": "https://venda.amazon.com.br/brand-registry"},
      {"text": "Ja tenho Brand Registry aprovado", "next": "sop_com_ean_marca"},
      {"text": "Quero listar enquanto espero aprovacao", "next": "sop_com_ean_marca"}
    ]
  },
  "sem_inpi_logo": {
    "question": "O nome ou logo da sua marca aparece NO produto?",
    "warning": "NAO pode ser adesivo, etiqueta colada ou costurado. Precisa estar impresso, gravado, bordado ou estampado diretamente no produto.",
    "options": [
      {"text": "Sim, aparece no produto (impresso/gravado)", "next": "sem_inpi_fotos"},
      {"text": "Nao aparece no produto", "next": "listar_generico_temp"}
    ]
  },
  "sem_inpi_fotos": {
    "question": "Voce consegue listar! Vai precisar comprovar com fotos.",
    "steps": [
      "Na hora de listar, o sistema vai pedir fotos do produto mostrando a marca",
      "Tire fotos claras onde aparece o nome/logo no produto",
      "E interessante ter embalagem com a marca tambem",
      "O processo pode levar alguns dias para aprovacao"
    ],
    "info": "Dica: tenha fotos de varios angulos mostrando a marca claramente.",
    "options": [
      {"text": "Entendi! Vamos listar", "next": "sop_com_ean_marca"},
      {"text": "Nao tenho fotos boas ainda", "next": "ajuda_final"}
    ]
  },
  "listar_generico_temp": {
    "question": "Sem marca visivel no produto, voce lista como generico por enquanto.",
    "info": "Voce pode listar como generico agora e depois, quando tiver o INPI aprovado, migrar para sua marca.",
    "options": [
      {"text": "Ok, vou listar como generico", "next": "sop_generico"},
      {"text": "Quero registrar minha marca primeiro", "link": "https://www.gov.br/inpi/pt-br"}
    ]
  },
  "revendedor_nf": {
    "question": "Voce tem Nota Fiscal com minimo 10 produtos dessa marca na MESMA NF?",
    "warning": "Precisa ser 10+ unidades na MESMA nota fiscal. Nao pode juntar notas diferentes.",
    "options": [
      {"text": "Sim, tenho NF com 10+ produtos", "next": "sop_com_ean_marca"},
      {"text": "Nao tenho NF com 10+", "next": "revendedor_sem_nf"}
    ]
  },
  "revendedor_sem_nf": {
    "question": "Sem NF com 10+ produtos, voce nao consegue autorizacao de marca.",
    "info": "Opcoes: comprar 10+ unidades do distribuidor na mesma NF, ou listar o produto sem vincular a marca (como generico).",
    "options": [
      {"text": "Vou comprar 10+ e voltar com a NF", "next": "inicio"},
      {"text": "Vou listar como generico por enquanto", "next": "sop_generico"}
    ]
  },
  "marca_pergunta": {
    "question": "Seu produto tem marca ou logo na embalagem ou no produto?",
    "info": "Impresso, gravado ou estampado. Adesivo ou costurado NAO conta.",
    "options": [
      {"text": "Sim, tem marca", "next": "marca_sua_ou_terceiro_sem_ean"},
      {"text": "Nao, sem marca (generico)", "next": "sop_generico"}
    ]
  },
  "marca_sua_ou_terceiro_sem_ean": {
    "question": "A marca e sua ou voce revende?",
    "options": [
      {"text": "Marca propria (eu sou o dono)", "next": "marca_propria_inpi_sem_ean"},
      {"text": "Revendo (marca de terceiro)", "next": "revendedor_sem_ean"}
    ]
  },
  "marca_propria_inpi_sem_ean": {
    "question": "Voce tem registro no INPI?",
    "options": [
      {"text": "Sim, tenho INPI aprovado", "next": "brand_registry_sem_ean"},
      {"text": "INPI em andamento", "next": "brand_registry_sem_ean"},
      {"text": "Nao tenho INPI", "next": "sem_inpi_logo_sem_ean"}
    ]
  },
  "brand_registry_sem_ean": {
    "question": "Registre sua marca na Amazon (Brand Registry)",
    "steps": [
      "Acesse o Brand Registry no link abaixo",
      "Cadastre com seu numero do INPI",
      "Aguarde aprovacao",
      "Depois liste usando Formulario em branco (sem EAN, voce pede isencao)"
    ],
    "options": [
      {"text": "Ir para o Brand Registry", "link": "https://venda.amazon.com.br/brand-registry"},
      {"text": "Ja tenho Brand Registry", "next": "sop_generico"},
      {"text": "Vou listar enquanto espero", "next": "sop_generico"}
    ]
  },
  "sem_inpi_logo_sem_ean": {
    "question": "O nome ou logo da sua marca aparece NO produto?",
    "warning": "NAO pode ser adesivo ou costurado. Precisa estar impresso/gravado no produto.",
    "options": [
      {"text": "Sim, aparece no produto", "next": "sem_inpi_fotos_sem_ean"},
      {"text": "Nao aparece", "next": "sop_generico"}
    ]
  },
  "sem_inpi_fotos_sem_ean": {
    "question": "Voce consegue listar! Vai comprovar com fotos.",
    "steps": [
      "O sistema vai pedir fotos mostrando a marca no produto",
      "Tire fotos claras de varios angulos",
      "Tenha embalagem com a marca tambem (se possivel)",
      "Pode levar alguns dias para aprovacao"
    ],
    "options": [
      {"text": "Entendi! Vamos listar", "next": "sop_generico"},
      {"text": "Preciso de ajuda", "next": "ajuda_final"}
    ]
  },
  "revendedor_sem_ean": {
    "question": "Revendedor sem EAN: voce precisa de NF com 10+ produtos da marca.",
    "warning": "Sem EAN e sem NF com 10+ produtos, nao e possivel listar vinculado a marca. Seria generico.",
    "options": [
      {"text": "Tenho NF com 10+ produtos", "next": "sop_generico"},
      {"text": "Nao tenho, vou listar como generico", "next": "sop_generico"},
      {"text": "Vou comprar 10+ e voltar", "next": "inicio"}
    ]
  },
  "sop_generico": {
    "question": "Passo a passo: Listar produto GENERICO (sem EAN)",
    "steps": [
      "No Seller Central, va em: Menu > Catalogo > Adicionar Produto",
      "Clique em 'Formulario em branco'",
      "Clique em 'Iniciar'",
      "Clique em 'Experimente agora' no botao preto - nossa IA vai te ajudar a preencher cerca de 80% dos campos",
      "Complete os campos restantes (fotos, preco, estoque)",
      "Clique em 'Salvar e publicar'"
    ],
    "info": "A IA da Amazon preenche titulo, descricao e atributos automaticamente. Voce so revisa e ajusta!",
    "options": [
      {"text": "Consegui listar!", "next": "sucesso"},
      {"text": "Deu erro na listagem", "next": "erros_menu"},
      {"text": "Nao encontro o Formulario em branco", "next": "ajuda_formulario"}
    ]
  },
  "sop_com_ean_generico": {
    "question": "Passo a passo: Listar com EAN (produto sem marca)",
    "steps": [
      "No Seller Central, va em: Menu > Catalogo > Adicionar Produto",
      "Na barra de busca, digite o EAN do produto",
      "Se ENCONTRAR: clique no produto e depois em 'Vender este produto'",
      "Se NAO ENCONTRAR: clique em 'Formulario em branco' e siga o processo",
      "Preencha preco, quantidade e metodo de envio",
      "Clique em 'Salvar e publicar'"
    ],
    "options": [
      {"text": "Encontrei o produto! Listei com sucesso", "next": "sucesso"},
      {"text": "Nao encontrou meu EAN", "next": "sop_generico"},
      {"text": "Pediu autorizacao de marca", "next": "autorizacao_marca"},
      {"text": "Deu outro erro", "next": "erros_menu"}
    ]
  },
  "sop_com_ean_marca": {
    "question": "Passo a passo: Listar com EAN e Marca",
    "steps": [
      "No Seller Central, va em: Menu > Catalogo > Adicionar Produto",
      "Na barra de busca, digite o EAN ou nome do produto",
      "Se ENCONTRAR: clique no produto > 'Vender este produto'",
      "Se pedir autorizacao: envie sua NF com 10+ produtos da marca",
      "Se NAO ENCONTRAR: va para 'Formulario em branco' e preencha com sua marca",
      "Clique em 'Salvar e publicar'"
    ],
    "options": [
      {"text": "Consegui listar!", "next": "sucesso"},
      {"text": "Pediu autorizacao de marca", "next": "autorizacao_marca"},
      {"text": "Deu erro", "next": "erros_menu"},
      {"text": "Nao encontro meu produto", "next": "sop_generico"}
    ]
  },
  "autorizacao_marca": {
    "question": "Pediu autorizacao de marca? Normal! Siga o processo:",
    "steps": [
      "O sistema vai direcionar voce para enviar documentos",
      "Envie sua NF com 10+ produtos da mesma marca (na MESMA NF)",
      "A NF precisa: ser dos ultimos 180 dias, estar legivel, ter CNPJ visivel",
      "Aguarde a analise (pode levar ate 5 dias uteis)",
      "Se aprovado: volte e liste normalmente"
    ],
    "options": [
      {"text": "Enviei a NF! Aprovaram", "next": "sop_com_ean_marca"},
      {"text": "Recusaram minha NF", "next": "nf_recusada"},
      {"text": "Estou aguardando resposta", "next": "aguardando_aprovacao"}
    ]
  },
  "nf_recusada": {
    "question": "NF recusada? Verifique esses pontos:",
    "steps": [
      "NF emitida nos ultimos 180 dias?",
      "Tem 10+ produtos da MESMA marca na MESMA NF?",
      "NF esta legivel (nao cortada, sem borroes)?",
      "CNPJ do vendedor e do fornecedor visiveis?",
      "Nome da marca aparece na descricao dos produtos?"
    ],
    "options": [
      {"text": "Corrigi e enviei novamente", "next": "aguardando_aprovacao"},
      {"text": "Tudo certo na NF e recusou mesmo assim", "next": "nf_recusada_tudo_certo"},
      {"text": "Nao tenho NF com 10+ produtos", "next": "revendedor_sem_nf"}
    ]
  },
  "nf_recusada_tudo_certo": {
    "question": "NF correta mas recusou? Abra um chamado:",
    "steps": [
      "Va em: Seller Central > Ajuda > Obter Ajuda",
      "Busque por 'autorizacao de marca'",
      "Localize o chamado aberto (tem um ID/numero)",
      "Clique em 'Responder' e peca mais clareza sobre o motivo da recusa",
      "Se nao resolver, fale com seu Account Manager"
    ],
    "options": [
      {"text": "Consegui resolver!", "next": "sop_com_ean_marca"},
      {"text": "Nao achei o chamado", "next": "ajuda_chamado"},
      {"text": "Preciso de mais ajuda", "next": "ajuda_final"}
    ]
  },
  "ajuda_chamado": {
    "question": "Como encontrar seu chamado:",
    "steps": [
      "Seller Central > Ajuda (canto superior direito)",
      "Clique em 'Obter Ajuda'",
      "Clique em 'Gerenciar ajuda' ou 'Meus chamados'",
      "Procure por 'Autorizacao de marca' na lista",
      "Clique para ver detalhes e responder"
    ],
    "options": [
      {"text": "Achei! Vou responder", "next": "aguardando_aprovacao"},
      {"text": "Ainda nao encontro", "next": "ajuda_final"}
    ]
  },
  "aguardando_aprovacao": {
    "question": "Aguardando aprovacao...",
    "info": "A analise pode levar ate 5 dias uteis. Enquanto isso, voce pode listar outros produtos que nao precisem de autorizacao.",
    "options": [
      {"text": "Aprovaram! Quero listar agora", "next": "sop_com_ean_marca"},
      {"text": "Recusaram de novo", "next": "nf_recusada"},
      {"text": "Quero listar outro produto enquanto espero", "next": "inicio"}
    ]
  },
  "ajuda_formulario": {
    "question": "Nao encontra o Formulario em branco?",
    "steps": [
      "Certifique-se de estar em: Menu > Catalogo > Adicionar Produto",
      "Na pagina de busca, role para baixo",
      "Procure o botao 'Formulario em branco' (pode estar embaixo da barra de busca)",
      "Se nao aparecer, tente limpar a busca primeiro"
    ],
    "options": [
      {"text": "Achei! Vou continuar", "next": "sop_generico"},
      {"text": "Ainda nao encontro", "next": "ajuda_final"}
    ]
  },
  "erros_menu": {
    "question": "Qual erro aconteceu?",
    "options": [
      {"text": "Imagem rejeitada", "next": "erro_imagem"},
      {"text": "EAN duplicado / ja existe", "next": "erro_ean_duplicado"},
      {"text": "Categoria restrita / precisa aprovacao", "next": "erro_categoria"},
      {"text": "Erro 5461 - atributo obrigatorio", "next": "erro_atributo"},
      {"text": "Produto bloqueado / suprimido", "next": "erro_bloqueado"},
      {"text": "Outro erro que nao sei resolver", "next": "ajuda_final"}
    ]
  },
  "erro_imagem": {
    "question": "Imagem rejeitada? Verifique:",
    "steps": [
      "Imagem principal: fundo BRANCO puro (RGB 255,255,255)",
      "Minimo 1000x1000 pixels (ideal 2000x2000)",
      "Produto ocupa 85% do espaco da foto",
      "Sem textos, logos, bordas ou marcas dagua",
      "Formato: JPEG, PNG ou TIFF",
      "Sem embalagem aparecendo (so o produto)"
    ],
    "options": [
      {"text": "Corrigi a imagem! Vou tentar de novo", "next": "sop_generico"},
      {"text": "Nao consigo fazer a foto certa", "next": "ajuda_final"}
    ]
  },
  "erro_ean_duplicado": {
    "question": "EAN duplicado / ja existe na Amazon?",
    "info": "Isso significa que alguem ja listou um produto com esse EAN. Voce pode se vincular ao produto existente.",
    "steps": [
      "Se o produto e o MESMO que voce vende: clique em 'Vender este produto'",
      "Se o produto listado e DIFERENTE do seu: abra um chamado pedindo correcao",
      "Se o EAN pertence a outra marca: voce nao pode usar esse EAN"
    ],
    "options": [
      {"text": "E o mesmo produto! Vou vender este", "next": "sucesso"},
      {"text": "O produto listado e diferente do meu", "next": "ajuda_final"},
      {"text": "Vou listar sem EAN (generico)", "next": "sop_generico"}
    ]
  },
  "erro_categoria": {
    "question": "Categoria restrita? Algumas categorias precisam de aprovacao.",
    "info": "Categorias como Saude, Beleza, Alimentos, Suplementos e Eletronicos podem exigir documentos extras.",
    "steps": [
      "Verifique qual documento e exigido (geralmente: NF, certificado ANVISA, INMETRO)",
      "Acesse: Seller Central > Ajuda > busque 'aprovar categoria'",
      "Envie os documentos solicitados",
      "Aguarde analise (3 a 10 dias uteis)"
    ],
    "options": [
      {"text": "Ver lista de categorias restritas", "link": "https://sellercentral.amazon.com.br/help/hub/reference/external/G200164330?locale=pt-BR"},
      {"text": "Aprovaram minha categoria!", "next": "sop_com_ean_marca"},
      {"text": "Preciso de ajuda com documentos", "next": "ajuda_final"}
    ]
  },
  "erro_atributo": {
    "question": "Erro 5461 - Atributo obrigatorio faltando",
    "info": "A Amazon exige alguns campos preenchidos. Os mais comuns que faltam:",
    "steps": [
      "Verifique se preencheu: Titulo, Marca, Fabricante",
      "Verifique: Numero da peca (pode colocar o EAN ou SKU)",
      "Verifique: Tipo de produto (categoria)",
      "Use a IA (botao 'Experimente agora') para preencher automaticamente"
    ],
    "options": [
      {"text": "Corrigi! Vou tentar de novo", "next": "sop_generico"},
      {"text": "Nao sei qual campo esta faltando", "next": "ajuda_final"}
    ]
  },
  "erro_bloqueado": {
    "question": "Produto bloqueado ou suprimido?",
    "info": "Isso pode acontecer por: produto restrito, violacao de propriedade intelectual, ou problema na conta.",
    "steps": [
      "Va em: Seller Central > Desempenho > Saude da conta",
      "Verifique se ha notificacoes sobre o bloqueio",
      "Leia o motivo e siga as instrucoes da Amazon",
      "Se nao entender o motivo, abra um chamado"
    ],
    "options": [
      {"text": "Resolvi o problema!", "next": "inicio"},
      {"text": "Nao entendo o motivo do bloqueio", "next": "ajuda_final"}
    ]
  },
  "usado": {
    "question": "Produtos usados/seminovos tem um programa especifico!",
    "info": "A Amazon tem o programa 'Amazon Seminovos' para produtos usados e recondicionados.",
    "options": [
      {"text": "Ir para Amazon Seminovos", "link": "https://venda.amazon.com.br/seminovos"},
      {"text": "Voltar ao inicio", "next": "inicio"}
    ]
  },
  "sucesso": {
    "question": "Parabens! Voce listou seu produto!",
    "info": "Seu produto pode levar ate 15 minutos para aparecer na Amazon. Enquanto isso, confira se tudo esta correto.",
    "steps": [
      "Verifique se o titulo esta claro e completo",
      "Confira se as imagens estao bonitas e em alta qualidade",
      "Revise o preco e quantidade em estoque",
      "Ative Ads para dar visibilidade ao seu produto"
    ],
    "options": [
      {"text": "Quero listar outro produto", "next": "inicio"},
      {"text": "Como ativar Ads?", "link": "https://advertising.amazon.com/pt-br"},
      {"text": "Como criar cupom/promocao?", "link": "https://sellercentral.amazon.com.br/merchandising"}
    ]
  },
  "ajuda_final": {
    "question": "Precisa de mais ajuda?",
    "info": "Sem problemas! Temos opcoes para te ajudar:",
    "options": [
      {"text": "Quero que listem pra mim (Listing Hub)", "link": "https://amazonexteu.qualtrics.com/jfe/form/SV_eEhccc2rqm5WURw"},
      {"text": "Falar com meu Account Manager", "next": "falar_am"},
      {"text": "Abrir chamado no Seller Central", "next": "abrir_chamado"},
      {"text": "Voltar ao inicio e tentar de novo", "next": "inicio"}
    ]
  },
  "falar_am": {
    "question": "Fale com seu Account Manager",
    "info": "Seu AM pode te ajudar com questoes mais complexas de listagem. Entre em contato pelo email ou telefone que voce ja tem.",
    "options": [
      {"text": "Voltar ao inicio", "next": "inicio"}
    ]
  },
  "abrir_chamado": {
    "question": "Como abrir um chamado:",
    "steps": [
      "Seller Central > Ajuda (canto superior direito)",
      "Clique em 'Obter Ajuda'",
      "Descreva seu problema detalhadamente",
      "Inclua: EAN, nome do produto, print do erro",
      "Aguarde resposta (geralmente 24-48h)"
    ],
    "options": [
      {"text": "Ir para Seller Central", "link": "https://sellercentral.amazon.com.br"},
      {"text": "Voltar ao inicio", "next": "inicio"}
    ]
  }
}

# Salvar arquivos
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html criado')

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(appjs)
print('js/app.js criado')

with open('data/flow.json', 'w', encoding='utf-8') as f:
    json.dump(flow, f, ensure_ascii=False, indent=2)
print('data/flow.json criado')

# CSS vazio (design ta inline no HTML)
with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write('/* Design inline no index.html */')
print('css/style.css criado')

# Validar JSON
try:
    json.loads(json.dumps(flow))
    total = len(flow)
    print(f'\nSUCESSO! {total} telas criadas e validadas!')
    print('Agora suba os arquivos pro GitHub e conecte no Netlify.')
except Exception as e:
    print(f'ERRO no JSON: {e}')

