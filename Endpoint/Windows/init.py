

from drives import add_honey_mapped_drives
from arp import add_honey_arp_cache

def main():
    try:
        add_honey_mapped_drives()
        add_honey_arp_cache()
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()