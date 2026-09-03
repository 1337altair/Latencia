from PySide6.QtCore import QSettings

translations = {
    "en": {
        "network_tools": "NETWORK TOOLS",
        "dashboard": "Dashboard",
        "monitor": "Monitor",
        "diagnostics": "Diagnostics",
        "history": "History",
        "settings": "Settings",
        "connection": "Connection",
        "connection_sub": "Check the current quality of your internet connection.",
        "ready": "READY",
        "running": "RUNNING",
        "online": "ONLINE",
        "error": "ERROR",
        "run_test": "RUN TEST",
        "testing_ping": "PING...",
        "testing_download": "DOWNLOAD...",
        "testing_upload": "UPLOAD...",
        "download": "DOWNLOAD",
        "upload": "UPLOAD",
        "ping": "PING",
        "jitter": "JITTER",
        "packet_loss": "PACKET LOSS",
        "score": "CONNECTION SCORE",
        "local_ip": "Local IP",
        "adapter": "Adapter",
        "unknown": "Unknown",
        "excellent": "Excellent",
        "good": "Good",
        "fair": "Fair",
        "poor": "Poor",
        "monitor_title": "Live monitor",
        "monitor_sub": "Track latency once per second.",
        "current_latency": "CURRENT LATENCY",
        "monitor_stopped": "Monitor stopped",
        "monitoring": "Monitoring 1.1.1.1",
        "start": "START",
        "stop": "STOP",
        "timeout": "Timeout",
        "diagnostics_title": "Diagnostics",
        "diagnostics_sub": "A quick look at latency and connection stability.",
        "no_diagnostic": "No diagnostic yet.",
        "run_diagnostics": "RUN DIAGNOSTICS",
        "history_title": "History",
        "history_sub": "Results saved from previous tests.",
        "date": "Date",
        "status": "Status",
        "settings_title": "Settings",
        "settings_sub": "Basic application preferences.",
        "language": "LANGUAGE",
        "language_help": "Interface language",
        "author": "AUTHOR",
        "high_loss": "High packet loss detected. The connection may be unstable.",
        "small_loss": "A small amount of packet loss was detected.",
        "high_ping": "Latency is high and may affect games and calls.",
        "mid_ping": "Latency is a little above ideal.",
        "high_jitter": "Jitter is high. Real-time traffic may feel unstable.",
        "mid_jitter": "Jitter is a little above ideal.",
        "all_good": "No major latency or stability problem was detected.",
        "test_failed": "Test failed"
    },
    "pt-BR": {
        "network_tools": "FERRAMENTAS DE REDE",
        "dashboard": "Painel",
        "monitor": "Monitor",
        "diagnostics": "Diagnóstico",
        "history": "Histórico",
        "settings": "Configurações",
        "connection": "Conexão",
        "connection_sub": "Veja como está a qualidade atual da sua internet.",
        "ready": "PRONTO",
        "running": "TESTANDO",
        "online": "ONLINE",
        "error": "ERRO",
        "run_test": "INICIAR TESTE",
        "testing_ping": "PING...",
        "testing_download": "DOWNLOAD...",
        "testing_upload": "UPLOAD...",
        "download": "DOWNLOAD",
        "upload": "UPLOAD",
        "ping": "PING",
        "jitter": "JITTER",
        "packet_loss": "PERDA DE PACOTES",
        "score": "NOTA DA CONEXÃO",
        "local_ip": "IP local",
        "adapter": "Adaptador",
        "unknown": "Desconhecido",
        "excellent": "Excelente",
        "good": "Boa",
        "fair": "Regular",
        "poor": "Ruim",
        "monitor_title": "Monitor em tempo real",
        "monitor_sub": "Acompanhe a latência da conexão a cada segundo.",
        "current_latency": "LATÊNCIA ATUAL",
        "monitor_stopped": "Monitor parado",
        "monitoring": "Monitorando 1.1.1.1",
        "start": "INICIAR",
        "stop": "PARAR",
        "timeout": "Sem resposta",
        "diagnostics_title": "Diagnóstico",
        "diagnostics_sub": "Uma análise rápida da latência e estabilidade da conexão.",
        "no_diagnostic": "Nenhum diagnóstico ainda.",
        "run_diagnostics": "EXECUTAR DIAGNÓSTICO",
        "history_title": "Histórico",
        "history_sub": "Resultados salvos dos testes anteriores.",
        "date": "Data",
        "status": "Status",
        "settings_title": "Configurações",
        "settings_sub": "Preferências básicas do aplicativo.",
        "language": "IDIOMA",
        "language_help": "Idioma da interface",
        "author": "AUTOR",
        "high_loss": "A perda de pacotes está alta. A conexão pode estar instável.",
        "small_loss": "Foi detectada uma pequena perda de pacotes.",
        "high_ping": "A latência está alta e pode atrapalhar jogos e chamadas.",
        "mid_ping": "A latência está um pouco acima do ideal.",
        "high_jitter": "O jitter está alto. Tráfego em tempo real pode ficar instável.",
        "mid_jitter": "O jitter está um pouco acima do ideal.",
        "all_good": "Nenhum problema importante de latência ou estabilidade foi detectado.",
        "test_failed": "Falha no teste"
    }
}

prefs = QSettings("0xaltair", "Latencia")
lang = prefs.value("language", "pt-BR")
if lang not in translations:
    lang = "pt-BR"


def t(key):
    return translations[lang].get(key, key)


def set_language(value):
    global lang
    if value in translations:
        lang = value
        prefs.setValue("language", value)


def get_language():
    return lang
