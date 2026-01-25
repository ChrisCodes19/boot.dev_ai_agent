from functions.get_file_content import get_file_content

def main():
    content = get_file_content("calculator", "lorem.txt")
    assert len(content) >= 10000
    expected_suffix = '[...File "lorem.txt" truncated at 10000 characters]'
    assert content.endswith(expected_suffix)
    print("lorem.txt passed")
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    main()