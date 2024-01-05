import os

def tools():
    try:
        complete_path = os.path.join(os.getcwd(), 'tools')
        path_content = os.listdir(complete_path)
        folders = [elem for elem in path_content if os.path.isdir(os.path.join(complete_path, elem))]
        
        return folders
    
    except Exception as e:
        print(f"Error: {e}")
        return []