# Add steps/actions here:

1. step 1  terraform init  to install the providers 

2. step 2   terraform destroy --target local_file.foo[4]  to destroy the second resource counting using index 

3. you cal laos use terraform state rm 'local_file.foo[4]' to remove it from state  
4.  then you can do a terraform state mv  source destination 
