"""
CLI script to initialize/reset default admin user
Usage: python init_admin.py
"""
import asyncio
import sys
from app.core.init_db import init_default_admin


async def main():
    """Main entry point"""
    print("=" * 60)
    print("Initializing Default Admin User")
    print("=" * 60)
    
    try:
        await init_default_admin()
        print("\n" + "=" * 60)
        print("✅ Initialization completed successfully!")
        print("=" * 60)
        return 0
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ Initialization failed: {str(e)}")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
