# Service environment declaration
host_list=['docker_master','docker_dev']
# docker hosts
log_tail_line=300
# Shows the number of rows from the tail
# service_name_list=['manage-service','job-service','trace-service','payment-service','message-service','user-service','order-service']
service_name_list=['manage','job','trace','payment','message','user','order']
# A service that serves a timed task to determine whether a service exists
log_dir_master  = '/Users/yunque/log_everyone_bak'
# Log on the host directory
key_address='/Users/yunque/.ssh/id_rsa'
# The key position