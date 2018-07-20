

from drives import add_honey_mapped_drives

def main():
    try:
        add_honey_mapped_drives()
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()