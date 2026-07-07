from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def write(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


def build_signal_panel() -> str:
    return r'''
<svg width="1200" height="360" viewBox="0 0 1200 360" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Build signal panel showing product engineering focus">
  <defs>
    <linearGradient id="frame" x1="60" y1="30" x2="1140" y2="330" gradientUnits="userSpaceOnUse">
      <stop stop-color="#00F6FF"/><stop offset=".52" stop-color="#7CA8FF"/><stop offset="1" stop-color="#FF2ED1"/>
    </linearGradient>
    <linearGradient id="cyanMag" x1="160" y1="180" x2="1040" y2="180" gradientUnits="userSpaceOnUse">
      <stop stop-color="#00F6FF"/><stop offset=".5" stop-color="#72C7FF"/><stop offset="1" stop-color="#FF2ED1"/>
    </linearGradient>
    <filter id="glow" x="-30%" y="-40%" width="160%" height="180%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <pattern id="grid" width="46" height="46" patternUnits="userSpaceOnUse">
      <path d="M0 23H46M23 0V46" stroke="#123240" stroke-width="1" opacity=".35"/>
    </pattern>
  </defs>
  <rect width="1200" height="360" fill="#080D14"/>
  <circle cx="250" cy="180" r="260" fill="#00F6FF" opacity=".13" filter="url(#soft)"/>
  <circle cx="930" cy="170" r="250" fill="#FF2ED1" opacity=".12" filter="url(#soft)"/>
  <rect width="1200" height="360" fill="url(#grid)" opacity=".4"/>
  <rect x="28" y="22" width="1144" height="316" rx="28" fill="none" stroke="url(#frame)" stroke-width="5" filter="url(#glow)" opacity=".45">
    <animate attributeName="opacity" values=".45;1;.45" dur="3.2s" calcMode="spline" keyTimes="0;.5;1" keySplines=".42 0 .58 1;.42 0 .58 1" repeatCount="indefinite"/>
  </rect>
  <rect x="28" y="22" width="1144" height="316" rx="28" fill="#0B111B" stroke="url(#frame)" stroke-width="2.5"/>
  <rect x="52" y="46" width="1096" height="268" rx="18" fill="#070B11" stroke="#607080" stroke-width="1" opacity=".9"/>
  <rect x="424" y="34" width="352" height="54" rx="27" fill="#07151B" stroke="#00F6FF" stroke-width="2" filter="url(#glow)"/>
  <text x="600" y="69" text-anchor="middle" font-family="Consolas, 'JetBrains Mono', monospace" font-size="25" font-weight="700" fill="#9DFBFF">&gt; build_signal --now</text>

  <path d="M178 184H1022" stroke="url(#cyanMag)" stroke-width="16" stroke-linecap="round" opacity=".18" filter="url(#glow)"/>
  <path d="M178 184H1022" stroke="url(#cyanMag)" stroke-width="3" stroke-linecap="round" stroke-dasharray="16 12" opacity=".95"/>

  <g font-family="Consolas, 'JetBrains Mono', monospace">
    <g transform="translate(106 114)">
      <rect width="246" height="142" rx="18" fill="#0A1720" stroke="#00F6FF" stroke-width="2" filter="url(#glow)"/>
      <text x="123" y="34" text-anchor="middle" font-size="18" font-weight="700" fill="#9DFBFF">PRODUCT MODE</text>
      <path d="M78 72H168M78 92H142M78 112H184" stroke="#DFFBFF" stroke-width="7" stroke-linecap="round" opacity=".9"/>
      <circle cx="58" cy="72" r="8" fill="#00F6FF"/><circle cx="58" cy="92" r="8" fill="#FF2ED1"/><circle cx="58" cy="112" r="8" fill="#87F7FF"/>
      <text x="123" y="132" text-anchor="middle" font-size="14" fill="#B8C7D4">IDEATE -> BUILD -> SHIP</text>
    </g>
    <g transform="translate(477 104)">
      <rect width="246" height="162" rx="20" fill="#11131F" stroke="#7CA8FF" stroke-width="2" filter="url(#glow)"/>
      <text x="123" y="36" text-anchor="middle" font-size="18" font-weight="700" fill="#B9D8FF">CURRENT STACK</text>
      <text x="123" y="78" text-anchor="middle" font-size="32" font-weight="800" fill="#FFFFFF">FLUTTER</text>
      <text x="123" y="112" text-anchor="middle" font-size="25" font-weight="800" fill="#00F6FF">MERN</text>
      <text x="123" y="142" text-anchor="middle" font-size="18" font-weight="700" fill="#FF9AF0">VISION + AI</text>
    </g>
    <g transform="translate(848 114)">
      <rect width="246" height="142" rx="18" fill="#1A0D1B" stroke="#FF2ED1" stroke-width="2" filter="url(#glow)"/>
      <text x="123" y="34" text-anchor="middle" font-size="18" font-weight="700" fill="#FFC5F4">OUTPUT</text>
      <path d="M72 82L122 54L174 82V130H72V82Z" fill="#111923" stroke="#EAFBFF" stroke-width="3"/>
      <path d="M122 54V101M72 82L122 111L174 82" stroke="#00F6FF" stroke-width="2" opacity=".8"/>
      <text x="123" y="132" text-anchor="middle" font-size="14" fill="#DCE8F2">REAL PRODUCTS, NOT DEMOS</text>
    </g>
  </g>

  <g font-family="Consolas, 'JetBrains Mono', monospace" font-size="15" fill="#DCE8F2">
    <rect x="236" y="286" width="728" height="34" rx="17" fill="#08131A" stroke="#324A5A"/>
    <text x="600" y="308" text-anchor="middle">status: building mobile, web, and intelligent systems that survive real users</text>
  </g>
</svg>
'''


def contact_panel() -> str:
    return r'''
<svg width="1200" height="300" viewBox="0 0 1200 300" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Connect panel with email LinkedIn and GitHub contact modules">
  <defs>
    <linearGradient id="metal" x1="80" y1="50" x2="1120" y2="260" gradientUnits="userSpaceOnUse">
      <stop stop-color="#394550"/><stop offset=".25" stop-color="#111820"/><stop offset=".7" stop-color="#202832"/><stop offset="1" stop-color="#4D2A48"/>
    </linearGradient>
    <linearGradient id="edge" x1="85" y1="55" x2="1115" y2="255" gradientUnits="userSpaceOnUse">
      <stop stop-color="#00F6FF"/><stop offset=".5" stop-color="#8796A5"/><stop offset="1" stop-color="#FF2ED1"/>
    </linearGradient>
    <linearGradient id="tube" x1="160" y1="135" x2="380" y2="135" gradientUnits="userSpaceOnUse">
      <stop stop-color="#06232A"/><stop offset=".5" stop-color="#33FFF0"/><stop offset="1" stop-color="#06171D"/>
    </linearGradient>
    <linearGradient id="magPlate" x1="460" y1="105" x2="755" y2="190" gradientUnits="userSpaceOnUse">
      <stop stop-color="#54415E"/><stop offset=".5" stop-color="#8A4F8B"/><stop offset="1" stop-color="#251B2F"/>
    </linearGradient>
    <filter id="glow" x="-35%" y="-50%" width="170%" height="200%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="blur" x="-20%" y="-30%" width="140%" height="160%"><feGaussianBlur stdDeviation="18"/></filter>
  </defs>
  <rect width="1200" height="300" fill="#070B10"/>
  <rect width="1200" height="300" fill="#0D1720"/>
  <circle cx="180" cy="120" r="170" fill="#00F6FF" opacity=".09" filter="url(#blur)"/>
  <circle cx="930" cy="100" r="180" fill="#FF2ED1" opacity=".08" filter="url(#blur)"/>
  <g opacity=".18" stroke="#9BA8B5" stroke-width="2">
    <path d="M24 230H190M920 44H1174M40 84H210M970 240H1160"/>
    <rect x="18" y="80" width="74" height="42" rx="8"/><rect x="1048" y="44" width="90" height="54" rx="9"/>
  </g>

  <rect x="88" y="50" width="1024" height="206" rx="24" fill="url(#metal)" stroke="#0B0D10" stroke-width="8"/>
  <rect x="102" y="64" width="996" height="178" rx="18" fill="none" stroke="url(#edge)" stroke-width="4" filter="url(#glow)" opacity=".42">
    <animate attributeName="opacity" values=".42;.95;.42" dur="3.7s" begin=".45s" calcMode="spline" keyTimes="0;.5;1" keySplines=".42 0 .58 1;.42 0 .58 1" repeatCount="indefinite"/>
  </rect>
  <rect x="102" y="64" width="996" height="178" rx="18" fill="#061018" stroke="url(#edge)" stroke-width="1.5"/>
  <rect x="123" y="84" width="954" height="134" rx="12" fill="#060B0F" stroke="#324452"/>
  <g fill="#071018" stroke="#A0A8B0" stroke-width="1.2">
    <circle cx="118" cy="72" r="8"/><circle cx="1082" cy="72" r="8"/><circle cx="118" cy="234" r="8"/><circle cx="1082" cy="234" r="8"/>
  </g>
  <g fill="#9BA8B5"><circle cx="118" cy="72" r="2"/><circle cx="1082" cy="72" r="2"/><circle cx="118" cy="234" r="2"/><circle cx="1082" cy="234" r="2"/></g>

  <rect x="334" y="12" width="532" height="66" rx="33" fill="#09232C" stroke="#6A7B86" stroke-width="5"/>
  <rect x="346" y="22" width="508" height="46" rx="23" fill="#07171F" stroke="#00F6FF" stroke-width="2" filter="url(#glow)"/>
  <text x="600" y="53" text-anchor="middle" font-family="Consolas, 'JetBrains Mono', monospace" font-size="26" font-weight="700" fill="#9DFBFF">&gt; connect --open-channel</text>

  <g stroke-linecap="round" fill="none">
    <path d="M380 143C426 143 430 143 462 143" stroke="#9DFBFF" stroke-width="14" opacity=".22"/>
    <path d="M380 132C425 132 430 132 462 132M380 154C425 154 430 154 462 154M754 132C795 132 800 132 822 132M754 154C795 154 800 154 822 154" stroke="#7EF7FF" stroke-width="3"/>
    <path d="M754 143C793 143 801 143 822 143" stroke="#FF73E6" stroke-width="10" opacity=".22"/>
  </g>

  <g font-family="Consolas, 'JetBrains Mono', monospace">
    <text x="270" y="98" text-anchor="middle" font-size="14" font-weight="700" fill="#DDE8EF">EMAIL</text>
    <rect x="150" y="105" width="240" height="86" rx="43" fill="url(#tube)" stroke="#B9D4DF" stroke-width="2" filter="url(#glow)"/>
    <rect x="144" y="110" width="36" height="76" rx="18" fill="#202B33" stroke="#8996A2" stroke-width="3"/>
    <rect x="360" y="110" width="36" height="76" rx="18" fill="#202B33" stroke="#8996A2" stroke-width="3"/>
    <path d="M224 137L270 164L316 137M224 137H316V169H224V137Z" stroke="#D9FFFF" stroke-width="5" filter="url(#glow)"/>
    <path d="M196 122H222M196 169H222M318 122H344M318 169H344M210 130H222M330 160H344" stroke="#B7FFFF" stroke-width="1.2" opacity=".75"/>
    <text x="270" y="181" text-anchor="middle" font-size="12" font-weight="700" fill="#C7FFFF">ASWABKHALIL@GMAIL.COM</text>

    <text x="608" y="98" text-anchor="middle" font-size="14" font-weight="700" fill="#DDE8EF">LINKEDIN</text>
    <rect x="438" y="91" width="340" height="110" rx="20" fill="#222831" stroke="#8896A5" stroke-width="4" filter="url(#glow)"/>
    <rect x="458" y="112" width="300" height="68" rx="10" fill="url(#magPlate)" stroke="#FFB3F4" stroke-width="2"/>
    <rect x="476" y="126" width="42" height="42" rx="7" fill="#281B2E" stroke="#9DFBFF" stroke-width="1.5"/>
    <text x="497" y="157" text-anchor="middle" font-size="33" font-family="Arial, sans-serif" font-weight="800" fill="#FFD5F7">in</text>
    <text x="534" y="135" font-size="15" font-weight="800" fill="#FFFFFF">MUHAMMAD ASWAB KHALIL</text>
    <text x="534" y="153" font-size="12" fill="#D2D8DF">aswabkhalil</text>
    <text x="534" y="169" font-size="12" fill="#D2D8DF">Connection + answabs</text>

    <rect x="889" y="80" width="86" height="22" rx="11" fill="#07131A" stroke="#00F6FF" stroke-width="1" opacity=".9"/>
    <text x="932" y="96" text-anchor="middle" font-size="15" font-weight="800" fill="#EAFBFF">GITHUB</text>
    <path d="M890 94H974L1034 143L974 196H890L830 143Z" fill="#091923" stroke="#00F6FF" stroke-width="3" filter="url(#glow)"/>
    <path d="M904 111H960L1001 143L960 178H904L863 143Z" fill="#10202A" stroke="#425968" stroke-width="1"/>
    <circle cx="932" cy="141" r="30" fill="#93FFFF"/>
    <path d="M910 120L902 106M954 120L962 106M905 142C905 126 918 116 932 116C946 116 959 126 959 142C959 161 946 169 932 169C918 169 905 161 905 142Z" fill="#9DFBFF" stroke="#0D3440" stroke-width="3"/>
    <circle cx="921" cy="142" r="5" fill="#063B46"/><circle cx="943" cy="142" r="5" fill="#063B46"/>
    <path d="M922 158C928 162 936 162 942 158" stroke="#063B46" stroke-width="3" stroke-linecap="round"/>
    <text x="932" y="188" text-anchor="middle" font-size="13" font-weight="800" fill="#DFFFFF">ASWAB007-OPS</text>
  </g>
</svg>
'''


def main() -> None:
    write(ASSETS / "build-signal-panel.svg", build_signal_panel())
    write(ASSETS / "contact-panel.svg", contact_panel())
    print("generated build-signal-panel.svg and contact-panel.svg")


if __name__ == "__main__":
    main()
