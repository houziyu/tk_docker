host_list=['docker_master','docker_node1','docker_node2']
#docker hosts
log_tail_line=300
#Shows the number of rows from the tail
#service_name_list=['manage-service','job-service','trace-service','payment-service','message-service','user-service','order-service']
service_name_list=['manage-service','job-service','trace-service','payment-service','message-service','user-service','order-service']
#A service that serves a timed task to determine whether a service exists
log_dir_master  = '/log_everyone_bak'
#Log on the host directory
key_address='/Users/yunque/.ssh/id_rsa'