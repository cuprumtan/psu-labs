 #!/bin/bash

case $1 in

	"help" ) xdg-open $(pwd)/README.html;;

	"kill-server" ) bash kill_server.sh;;

 	"kill-chat" ) bash kill_chat.sh;;

	"run-server" )

		#preps
		bash install_packages.sh

		#run server
		bash run_server.sh

		#open web
		xdg-open http://localhost:7071
		;;

	"chat" ) 
		
		#preps
		bash install_packages.sh

		#run chat
		bash run_client.sh

		#open web
		echo ""
		echo "Scanning network..."
		echo ""
		bash browse.sh localhost
		#xdg-open http://localhost:7070
		;;

	"attach" ) 
		
		#preps
		bash install_packages.sh

		#run chat
		bash run_chat.sh
		;;	

	"status" ) 

 		# chat
 		echo "chat status:"
 		lsof -i :7070

 		# file server
 		echo "server status:"
 		lsof -i :7071;;

	* )

		echo "Sorry, invalid command."

esac
