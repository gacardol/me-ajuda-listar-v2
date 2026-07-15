var SHEETDB_URL = "https://sheetdb.io/api/v1/7x95jmwaouxrl";
var flowData = {};
var historico = [];
var contato = "";

function dataAgora() {
  var d = new Date();
  var dia = ("0"+d.getDate()).slice(-2);
  var mes = ("0"+(d.getMonth()+1)).slice(-2);
  var ano = d.getFullYear();
  var hora = ("0"+d.getHours()).slice(-2);
  var min = ("0"+d.getMinutes()).slice(-2);
  return dia+"/"+mes+"/"+ano+" "+hora+":"+min;
}

function init() {
  fetch("flow.json")
    .then(function(r) { return r.json(); })
    .then(function(d) { flowData = d; pedirContato(); })
    .catch(function() {
      document.getElementById("app").innerHTML = "<div class=\"card\"><h2>Erro</h2><p>Nao foi possivel carregar. Recarregue a pagina.</p></div>";
    });
}

function pedirContato() {
  var h = "<div class=\"card\">";
  h += "<div class=\"logo\">Me Ajuda a Listar</div>";
  h += "<h2>Ola! Vou te ajudar a listar seu produto na Amazon</h2>";
  h += "<p>Primeiro, me deixe um dado de contato para te ajudarmos se precisar.</p>";
  h += "<p class=\"highlight\">100% gratuito!</p>";
  h += "<input id=\"contato\" class=\"input-field\" type=\"text\" placeholder=\"WhatsApp com DDD ou Nome da Loja\" />";
  h += "<p id=\"erro\" class=\"error-msg\">Por favor, digite seu WhatsApp ou Nome da Loja para continuar</p>";
  h += "<button class=\"btn-primary\" onclick=\"comecar()\">Comecar!</button>";
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
      body: JSON.stringify({data: {whatsapp: v, observacao: "acessou", tela: "inicio", data_hora: dataAgora()}})
    });
  } catch(e) {}
  mostrarTela("inicio");
}

function mostrarTela(id) {
  var s = flowData[id];
  if (!s) { document.getElementById("app").innerHTML = "<div class=\"card\"><h2>Ops!</h2><p>Tela nao encontrada. Volte ao inicio.</p></div>"; return; }
  historico.push(id);

  var h = "<div class=\"card\">";
  h += "<h2>" + s.question + "</h2>";

  if (s.info) { h += "<div class=\"info-box\">" + s.info + "</div>"; }
  if (s.warning) { h += "<div class=\"warning-box\">" + s.warning + "</div>"; }

  if (s.steps) {
    h += "<div class=\"steps\">";
    for (var i = 0; i < s.steps.length; i++) {
      h += "<div class=\"step\"><strong>" + (i+1) + ".</strong> " + s.steps[i] + "</div>";
    }
    h += "</div>";
  }

  if (s.options) {
    for (var j = 0; j < s.options.length; j++) {
      var o = s.options[j];
      if (o.link) {
        h += "<a class=\"btn-link\" href=\"" + o.link + "\" target=\"_blank\">" + o.text + "</a>";
      } else {
        h += "<button class=\"btn-option\" onclick=\"mostrarTela('" + o.next + "')\">" + o.text + "</button>";
      }
    }
  }

  if (historico.length > 1) {
    h += "<div class=\"footer-nav\">";
    h += "<button class=\"footer-btn\" onclick=\"voltar()\">Voltar</button>";
    h += "<button class=\"footer-btn\" onclick=\"mostrarTela('inicio')\">Inicio</button>";
    h += "<a class=\"footer-link\" href=\"https://amazonexteu.qualtrics.com/jfe/form/SV_eEhccc2rqm5WURw\" target=\"_blank\">Lista pra mim</a>";
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

init();
