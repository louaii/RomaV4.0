from header import _head, head_
import dependencies_check
import check_local
import sys

def main():
    
    if not dependencies_check.check_internet_connection:
        print("\033[1;31m!!!No Connection!!!\033[0m")
        head_()
        sys.exit()        
    else: 
        dependencies_check.check_dependencies(dependencies_check.required_dependencies)
        check_local.print_local()
        _head()
        


if __name__ == "__main__":
    main()
