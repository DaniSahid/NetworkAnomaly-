import streamlit as st
import re

st.set_page_config(page_title="Network Anomaly Explainer", page_icon="🔍", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #050d1a !important;
    color: #c9d8f0 !important;
}

/* ── App background ── */
.stApp {
    background: linear-gradient(160deg, #050d1a 0%, #0a1628 60%, #061020 100%);
}

/* ── Title & text ── */
h1, h2, h3, h4 { color: #7eb8f7 !important; letter-spacing: 0.5px; }
p, li, label, caption { color: #a8c4e0 !important; }
.stCaption, small { color: #5a7a9a !important; }

/* ── Divider ── */
hr { border-color: #1a3a5c !important; }

/* ── Radio buttons ── */
.stRadio label { color: #a8c4e0 !important; }
.stRadio [data-baseweb="radio"] div { border-color: #2a5a8a !important; }

/* ── Text input ── */
.stTextInput input {
    background: #0a1e35 !important;
    border: 1px solid #1e4a7a !important;
    border-radius: 6px !important;
    color: #c9d8f0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
.stTextInput input:focus {
    border-color: #3a8ae0 !important;
    box-shadow: 0 0 0 2px rgba(58,138,224,0.2) !important;
}
.stTextInput input::placeholder { color: #3a5a7a !important; }
.stTextInput label { color: #7eb8f7 !important; font-size: 13px !important; }

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #0f3460 0%, #1a5296 100%) !important;
    color: #e8f4ff !important;
    border: 1px solid #2a6abf !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    padding: 0.4rem 1.5rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1a5296 0%, #2a7ad4 100%) !important;
    border-color: #4a9ae0 !important;
    box-shadow: 0 0 12px rgba(58,138,224,0.4) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #0a1e35 !important;
    border: 1px solid #1a3a5c !important;
    border-radius: 6px !important;
    color: #7eb8f7 !important;
    font-size: 13px !important;
}
.streamlit-expanderContent {
    background: #070f1e !important;
    border: 1px solid #1a3a5c !important;
    border-top: none !important;
}

/* ── Info / Warning / Error native boxes ── */
.stAlert {
    background: #0a1e35 !important;
    border-color: #2a6abf !important;
    color: #a8c4e0 !important;
}

/* ── Result cards ── */
.result-danger {
    background: linear-gradient(135deg, #1a0810 0%, #120510 100%);
    border-left: 4px solid #e53e3e;
    border-top: 1px solid #3a1020;
    border-right: 1px solid #3a1020;
    border-bottom: 1px solid #3a1020;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin-bottom: 10px;
    color: #fca5a5;
    box-shadow: 0 0 20px rgba(229,62,62,0.12), inset 0 0 20px rgba(229,62,62,0.04);
}
.result-safe {
    background: linear-gradient(135deg, #081a12 0%, #051210 100%);
    border-left: 4px solid #22c55e;
    border-top: 1px solid #103a20;
    border-right: 1px solid #103a20;
    border-bottom: 1px solid #103a20;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin-bottom: 10px;
    color: #86efac;
    box-shadow: 0 0 20px rgba(34,197,94,0.10), inset 0 0 20px rgba(34,197,94,0.04);
}
.result-warning {
    background: linear-gradient(135deg, #1a1205 0%, #120e03 100%);
    border-left: 4px solid #f59e0b;
    border-top: 1px solid #3a2e10;
    border-right: 1px solid #3a2e10;
    border-bottom: 1px solid #3a2e10;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin-bottom: 10px;
    color: #fcd34d;
    box-shadow: 0 0 20px rgba(245,158,11,0.10), inset 0 0 20px rgba(245,158,11,0.04);
}
.result-info {
    background: linear-gradient(135deg, #071428 0%, #050e1e 100%);
    border-left: 4px solid #3b82f6;
    border-top: 1px solid #1a3a6a;
    border-right: 1px solid #1a3a6a;
    border-bottom: 1px solid #1a3a6a;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin-bottom: 10px;
    color: #93c5fd;
    box-shadow: 0 0 20px rgba(59,130,246,0.12), inset 0 0 20px rgba(59,130,246,0.04);
}

/* ── Markdown tables ── */
table {
    background: #0a1628 !important;
    border-collapse: collapse !important;
    width: 100% !important;
    font-size: 13px !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
th {
    background: #0f2040 !important;
    color: #7eb8f7 !important;
    padding: 8px 12px !important;
    border: 1px solid #1a3a5c !important;
    text-transform: uppercase !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
}
td {
    color: #a8c4e0 !important;
    padding: 7px 12px !important;
    border: 1px solid #122030 !important;
}
tr:nth-child(even) td { background: #071020 !important; }
tr:hover td { background: #0f2540 !important; }

/* ── Code inline ── */
code {
    background: #0f2040 !important;
    color: #7eb8f7 !important;
    border: 1px solid #1a3a5c !important;
    border-radius: 3px !important;
    padding: 1px 5px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Data ─────────────────────────────────────────────────────────────────────────

KNOWN_PORTS = {
    20:    ("FTP Data",            "normal",  "File transfer data channel. Normal if you use FTP servers."),
    21:    ("FTP Control",         "warning", "File transfer control. Unencrypted — prefer SFTP (port 22)."),
    22:    ("SSH",                 "normal",  "Secure remote login. Normal for servers and developers."),
    23:    ("Telnet",              "danger",  "Unencrypted remote login. Obsolete and insecure — should never be open."),
    25:    ("SMTP",                "warning", "Email sending. Open on end-user machines may indicate spam malware."),
    53:    ("DNS",                 "normal",  "Domain name resolution. Normal for all internet traffic."),
    67:    ("DHCP Server",         "normal",  "Assigns IP addresses on local networks. Normal for routers."),
    68:    ("DHCP Client",         "normal",  "Receives IP assignments. Normal for all devices."),
    80:    ("HTTP",                "warning", "Unencrypted web traffic. Normal but prefer HTTPS (443)."),
    110:   ("POP3",                "warning", "Email retrieval, unencrypted. Prefer IMAPS (993)."),
    135:   ("MS RPC",              "danger",  "Windows remote procedure calls. Common malware and ransomware target."),
    137:   ("NetBIOS",             "danger",  "Windows file sharing. Should not be exposed to the internet."),
    138:   ("NetBIOS Datagram",    "danger",  "Windows network browsing. Frequent attack target."),
    139:   ("NetBIOS Session",     "danger",  "Windows file/print sharing. Major ransomware entry point."),
    143:   ("IMAP",                "warning", "Email retrieval, unencrypted. Prefer IMAPS (993)."),
    161:   ("SNMP",                "danger",  "Network device management. Exposed to the internet is a serious risk."),
    194:   ("IRC",                 "danger",  "Internet Relay Chat. Historically used by botnets for command and control."),
    389:   ("LDAP",                "warning", "Directory services. Sensitive — should not be public-facing."),
    443:   ("HTTPS",               "normal",  "Encrypted web traffic. Expected on all web servers."),
    445:   ("SMB",                 "danger",  "Windows file sharing. Primary vector for WannaCry and NotPetya ransomware."),
    465:   ("SMTPS",               "normal",  "Encrypted email sending. Normal for mail servers."),
    500:   ("IKE / VPN",           "normal",  "VPN key exchange. Normal if you run a VPN server."),
    514:   ("Syslog",              "warning", "System logs. Should not be exposed publicly — can leak sensitive info."),
    587:   ("SMTP Submission",     "normal",  "Authenticated email sending. Standard for mail clients."),
    631:   ("IPP Printing",        "warning", "Internet printing protocol. Should not be exposed to the internet."),
    993:   ("IMAPS",               "normal",  "Encrypted email retrieval. Preferred over IMAP (143)."),
    995:   ("POP3S",               "normal",  "Encrypted email retrieval. Preferred over POP3 (110)."),
    1080:  ("SOCKS Proxy",         "danger",  "Proxy protocol. Commonly used by malware to tunnel traffic."),
    1194:  ("OpenVPN",             "normal",  "Open-source VPN. Normal if you run an OpenVPN server."),
    1433:  ("MS SQL Server",       "danger",  "Microsoft SQL database. Should never be exposed to the internet."),
    1434:  ("MS SQL Monitor",      "danger",  "SQL Server browser service. Frequent attack target."),
    1723:  ("PPTP VPN",            "warning", "Older VPN protocol with known weaknesses. Prefer OpenVPN or WireGuard."),
    3306:  ("MySQL",               "danger",  "MySQL database. Should never be directly exposed to the internet."),
    3389:  ("RDP",                 "danger",  "Windows Remote Desktop. Extremely common ransomware and brute-force target."),
    4444:  ("Metasploit Default",  "danger",  "Default port for Metasploit payloads. Almost never legitimate."),
    4899:  ("Radmin",              "danger",  "Remote admin tool. Has been used as a backdoor by attackers."),
    5432:  ("PostgreSQL",          "danger",  "PostgreSQL database. Should not be exposed to the internet."),
    5900:  ("VNC",                 "danger",  "Remote desktop. Often unencrypted and easily brute-forced. Use a VPN tunnel instead."),
    6660:  ("IRC",                 "danger",  "IRC port range commonly used by botnets."),
    6667:  ("IRC",                 "danger",  "Standard IRC port. Common botnet command-and-control channel."),
    6881:  ("BitTorrent",          "warning", "Peer-to-peer file sharing. May indicate unauthorised use on a network."),
    8080:  ("HTTP Alternate",      "warning", "Alternative web port. Normal for dev servers, suspicious on end-user machines."),
    8443:  ("HTTPS Alternate",     "normal",  "Alternative HTTPS port. Common for web apps and admin panels."),
    9001:  ("Tor",                 "warning", "Tor relay port. May indicate Tor usage on the network."),
    9050:  ("Tor SOCKS",           "warning", "Tor SOCKS proxy. Indicates Tor browser or client is running."),
    27017: ("MongoDB",             "danger",  "MongoDB database. Many exposed instances have been ransomed. Never public-facing."),
    31337: ("Back Orifice",        "danger",  "Classic backdoor/RAT port. No legitimate use."),
    65535: ("Reserved/Suspicious", "danger",  "Highest valid port. Commonly used by malware to avoid detection."),
}

PRIVATE_RANGES = [
    ("10.0.0.0",    "10.255.255.255",  "Private (Class A)",  "normal",  "Internal network address. Not routable on the internet."),
    ("172.16.0.0",  "172.31.255.255",  "Private (Class B)",  "normal",  "Internal network address. Not routable on the internet."),
    ("192.168.0.0", "192.168.255.255", "Private (Class C)",  "normal",  "Home/office network address. Not routable on the internet."),
    ("127.0.0.0",   "127.255.255.255", "Loopback",           "normal",  "Localhost. Traffic stays on your own machine."),
    ("169.254.0.0", "169.254.255.255", "Link-local (APIPA)", "warning", "Auto-assigned when DHCP fails. May indicate a network configuration issue."),
    ("0.0.0.0",     "0.255.255.255",   "Reserved",           "warning", "Reserved range. Should not appear as a source or destination."),
    ("224.0.0.0",   "239.255.255.255", "Multicast",          "normal",  "Used for group communications (e.g. mDNS, SSDP). Normal on LANs."),
    ("240.0.0.0",   "255.255.255.255", "Reserved/Broadcast", "warning", "Reserved by IANA. Seeing this as a destination may indicate scanning."),
]

STATUS_COLOR = {"normal": "#22c55e", "warning": "#f59e0b", "danger": "#e53e3e"}
STATUS_BOX   = {"normal": "result-safe", "warning": "result-warning", "danger": "result-danger"}
STATUS_LABEL = {"normal": "Normal", "warning": "Suspicious", "danger": "High Risk"}


# ── Helpers ───────────────────────────────────────────────────────────────────────

def ip_to_int(ip: str):
    parts = ip.split(".")
    return (int(parts[0]) << 24) | (int(parts[1]) << 16) | (int(parts[2]) << 8) | int(parts[3])

def classify_ip(ip: str):
    try:
        val = ip_to_int(ip)
    except Exception:
        return None
    for start, end, label, status, desc in PRIVATE_RANGES:
        if ip_to_int(start) <= val <= ip_to_int(end):
            return label, status, desc
    return "Public IP", "warning", "Routable on the internet. Could be legitimate or malicious — context matters."

def classify_port(port: int):
    if port in KNOWN_PORTS:
        return KNOWN_PORTS[port]
    if 0 <= port <= 1023:
        return "Well-known port (unlisted)", "normal", "System/well-known port range. Likely a standard service."
    if 1024 <= port <= 49151:
        return "Registered port (unlisted)", "normal", "Registered application port. Likely a legitimate application."
    if 49152 <= port <= 65535:
        return "Ephemeral/dynamic port", "normal", "Temporary port assigned by the OS for outbound connections. Usually normal."
    return "Invalid port", "danger", "Port number out of valid range (0–65535)."


# ── UI ────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div style="
    background: linear-gradient(135deg, #0a1e3a 0%, #0d2545 100%);
    border: 1px solid #1a3a6a;
    border-radius: 10px;
    padding: 24px 28px 18px 28px;
    margin-bottom: 24px;
    box-shadow: 0 0 40px rgba(59,130,246,0.08);
">
    <div style="font-family:'IBM Plex Mono',monospace; font-size:11px; color:#3b82f6; letter-spacing:3px; text-transform:uppercase; margin-bottom:6px;">
        CSC662 - Computer Security · Assignment
    </div>
    <h1 style="color:#7eb8f7; font-size:28px; margin:0 0 6px 0; font-family:'IBM Plex Sans',sans-serif; font-weight:700;">
        Network Anomaly Explainer
    </h1>
    <p style="color:#5a8ab0; font-size:14px; margin:0;">
        Analyse an IP address or port number — understand what it does, whether it poses a risk,
        and what attackers commonly use it for.
    </p>
</div>
""", unsafe_allow_html=True)

st.caption("All analysis runs locally. No data is sent anywhere.")
st.divider()

mode_net = st.radio("What do you want to check?", ["IP Address", "Port Number", "Both"], horizontal=True)
st.markdown("")

ip_input   = ""
port_input = ""

if mode_net in ("IP Address", "Both"):
    ip_input = st.text_input("IP Address", placeholder="e.g. 192.168.1.1  or  192.168.1.1:443")

if mode_net in ("Port Number", "Both"):
    port_input = st.text_input("Port Number", placeholder="e.g. 3389  or  443")

net_btn = st.button("Analyse", type="primary", key="net_btn")

if net_btn:
    if not ip_input and not port_input:
        st.warning("Please enter an IP address or port number.")
    else:
        # ── IP result ─────────────────────────────────────────────────────────
        if ip_input:
            ip = ip_input.strip()
            # Auto-strip port if user pastes from netstat e.g. "192.168.1.1:443"
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$', ip):
                ip, detected_port = ip.rsplit(":", 1)
                st.markdown(
                    f'<div class="result-info">Port <code>{detected_port}</code> detected in input — '
                    f'analysing IP <code>{ip}</code> and port separately.</div>',
                    unsafe_allow_html=True
                )
                port_input = detected_port

            ipv4 = re.match(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$', ip)
            if not ipv4 or not all(0 <= int(g) <= 255 for g in ipv4.groups()):
                st.error(f'"{ip}" is not a valid IPv4 address.')
            else:
                result = classify_ip(ip)
                if result:
                    label, status, desc = result
                    st.markdown(
                        f'<div class="{STATUS_BOX[status]}">'
                        f'<span style="font-family:\'IBM Plex Mono\',monospace;font-size:15px;font-weight:600;">{ip}</span>'
                        f'&nbsp;&nbsp;<span style="color:{STATUS_COLOR[status]};font-weight:700;font-size:13px;">'
                        f'[ {STATUS_LABEL[status]} ]</span>&nbsp;&nbsp;'
                        f'<span style="font-size:13px;opacity:0.8;">{label}</span><br>'
                        f'<span style="font-size:13px;margin-top:4px;display:block;">{desc}</span>'
                        f'</div>', unsafe_allow_html=True
                    )
                    if label == "Public IP":
                        octets = list(map(int, ip.split(".")))
                        if ip.endswith(".0") or ip.endswith(".255"):
                            st.caption("Note: This looks like a network or broadcast address — not typically assigned to a device.")
                        if octets[0] in (1, 2):
                            st.caption("Note: Low first octet — sometimes seen in network scanning traffic.")

        # ── Port result ───────────────────────────────────────────────────────
        if port_input:
            try:
                port = int(str(port_input).strip())
                name, status, desc = classify_port(port)
                st.markdown(
                    f'<div class="{STATUS_BOX[status]}">'
                    f'<span style="font-family:\'IBM Plex Mono\',monospace;font-size:15px;font-weight:600;">:{port}</span>'
                    f'&nbsp;&nbsp;<span style="color:{STATUS_COLOR[status]};font-weight:700;font-size:13px;">'
                    f'[ {STATUS_LABEL[status]} ]</span>&nbsp;&nbsp;'
                    f'<span style="font-size:13px;opacity:0.8;">{name}</span><br>'
                    f'<span style="font-size:13px;margin-top:4px;display:block;">{desc}</span>'
                    f'</div>', unsafe_allow_html=True
                )
            except ValueError:
                st.error("Port must be a whole number between 0 and 65535.")

st.divider()

# ── Quick reference ───────────────────────────────────────────────────────────────
with st.expander("High-risk ports — quick reference"):
    danger_ports = {p: v for p, v in KNOWN_PORTS.items() if v[1] == "danger"}
    rows = [f"| `{p}` | {v[0]} | {v[2]} |" for p, v in sorted(danger_ports.items())]
    st.markdown("| Port | Service | Why it's risky |\n|---|---|---|\n" + "\n".join(rows), unsafe_allow_html=True)

with st.expander("Private IP ranges — quick reference"):
    for start, end, label, _, desc in PRIVATE_RANGES:
        st.markdown(f"- **{start} – {end}** ({label}): {desc}")

with st.expander("How to read the results"):
    st.markdown("""
- **[ Normal ]** — expected traffic for a standard service or private network.
- **[ Suspicious ]** — not necessarily malicious, but warrants closer inspection.
- **[ High Risk ]** — commonly exploited by attackers, malware, or ransomware. Investigate immediately if seen unexpectedly.

**Get real data from your own machine:**
- Windows: run `netstat -ano` in Command Prompt — copy any `IP:port` entry directly into the IP field above.
- macOS/Linux: run `ss -tuln` or `netstat -tuln` in Terminal.
""")
