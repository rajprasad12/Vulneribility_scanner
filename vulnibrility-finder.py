import scanner


target_url= 'http://testphp.vulnweb.com/login.php'

input={'uname':'test', 'pass':'test', 'login':'submit'}
vul_scan= scanner.Scanner(target_url)
vul_scan.session.post(target_url, data=input)
vul_scan.extract_links()
vul_scan.run_scanner() 
