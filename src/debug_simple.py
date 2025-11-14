#!/usr/bin/env python3
print("🎯 СТАРТ ПРОГРАММЫ")

try:
    # Пробуем самый простой код
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--package', '-p', required=True)
    parser.add_argument('--source', '-s', required=True)
    parser.add_argument('--test-mode', action='store_true')

    args = parser.parse_args()

    print("✅ Аргументы распарсены:")
    print(f"   Package: {args.package}")
    print(f"   Source: {args.source}")
    print(f"   Test mode: {args.test_mode}")

except Exception as e:
    print(f"❌ ОШИБКА: {e}")
    import traceback

    traceback.print_exc()

print("🎯 КОНЕЦ ПРОГРАММЫ")