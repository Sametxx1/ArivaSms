# main.py
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import time
import random
import inspect
from sms import SendSms

from rich.console import Console
from rich.align import Align
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

def banner():
    title = Text()
    title.append("ARİVA ", style="bold cyan on black")
    title.append("SMS ", style="bold magenta on black")
    title.append("V2", style="bold yellow on black")
    console.print(
        Panel(
            Align.center(title, vertical="middle"),
            title="<<< ARİVA SMS V2 >>>",
            border_style="bright_green",
            box=box.DOUBLE_EDGE,
            padding=(1, 4),
        )
    )
    console.print(
        Panel(
            "Eğitim amaçlıdır. Kötüye kullanımdan kullanıcı sorumludur.",
            style="italic dim",
            box=box.SIMPLE,
        )
    )

def run_once(phone: str):
    sms = SendSms(phone, "")
    methods = [
        (name, method)
        for name, method in inspect.getmembers(sms, predicate=inspect.ismethod)
        if not name.startswith("__")
    ]
    results = []

    with console.status("[bold cyan]Gönderimler gerçekleştiriliyor...[/bold cyan]", spinner="dots"):
        for name, method in methods:
            try:
                method()
                results.append((name, True))
            except Exception as e:
                console.log(f"[red]Hata:[/] {name} -> {e}")
                results.append((name, False))
            time.sleep(random.uniform(0.2, 0.5))

    # Özet tablo
    table = Table(title="Gönderim Sonuçları", box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("Servis", style="cyan", no_wrap=True)
    table.add_column("Durum", style="bold")
    for svc, ok in results:
        status = "[green]Başarılı[/green]" if ok else "[red]Başarısız[/red]"
        table.add_row(svc, status)
    console.print(table)

    succ = sum(1 for _, ok in results if ok)
    fail = len(results) - succ
    console.print(
        Panel(
            f"✔ Başarılı: {succ}    ✖ Başarısız: {fail}",
            border_style="green",
            box=box.ROUNDED,
        )
    )

def main():
    console.clear()
    banner()
    phone = Prompt.ask("[bold yellow]Telefon numarasını girin[/bold yellow]", default="5051234567")
    console.print(f"\n[bold green]Başlıyor:[/] {phone}\n")

    try:
        while True:
            run_once(phone)
            console.print("\n[bold blue]5 saniye sonra yeniden çalışacak... (Çıkmak için Ctrl+C)[/bold blue]\n")
            time.sleep(5)
    except KeyboardInterrupt:
        console.print("\n[bold red]İşlem kullanıcı tarafından sonlandırıldı.[/bold red]")

if __name__ == "__main__":
    main()
