import os
import time

def load_config():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base, 'config.txt')
    example_path = os.path.join(base, 'config.example.txt')
    
    config = {
        'AI_PROVIDER': 'cloudflare',
        'CF_ACCOUNT_ID': '',
        'CF_API_TOKEN': '',
        'ASSISTANT_NAME': 'D.E.E.P.',
        'TYPO_SPEED': '0.01',
        'BOX_WIDTH': '66',
        'GITHUB_REPO': 'sulgai764-tech/DEEP-Assistant'
    }
    
    if not os.path.exists(config_path) and os.path.exists(example_path):
        import shutil
        shutil.copy(example_path, config_path)
        print("\n  [*] Создан config.txt. Впишите ключи Cloudflare!")
        time.sleep(2)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except:
        pass
    
    return config