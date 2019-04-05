#!/bin/bash

#################################################################################
###### cuprumtan 2019.04.04 #####################################################
#################################################################################

#################################################################################

case $1 in

	"kill-server" ) bash kill_server.sh;;

	"run-server" )

		echo "                                          .                               "
		echo "                              . -#+ .    ##.                              "
		echo "                                :###=. ####                               "
		echo "                                  *###=. .    .                           "
		echo "                           %### ... *###=   =###                          "
		echo "                      .  .  .##- ###- +## +###*.   .                      "
		echo "                      .##...   ####  .  +###+.... ##@.                    "
		echo "                       @###. +### :##  ###+ ##+ .###                      "
		echo "                .  -     @###- .   ####.    +###+.  .   -.                "
		echo "                . #### ..  @###-. ...####. .. =###*. .###+                "
		echo "                   .#: ####..%#.+###.. #= ####  +#..####                  "
		echo "                   . ####.    =###+. .  ####.    .####.                   "
		echo "                 . #### .### *##= =##-.###..###. ### *##%                 "
		echo "                  ###.   .#### .   @###-.    ####.    =###                "
		echo "                      . :# -###=. #%.####. .#. ####  .                    "
		echo "                      .###%     ####     .####   ####                     "
		echo "                      ...     ####. .  .#### . .   +                      "
		echo "                            ####. ####.@## .###-                          "
		echo "                           *##  .  .####..  .###                          "
		echo "                                 .## -####..                              "
		echo "                               .####   -###.                              "
		echo ""
		echo "           .╔══╗.     . ══.     ╔═  . ═╗             .                    "
		echo "            ║++.     ..++++   ..║+++  +║  ╔++╦═+++╦══╦**╦╗╔╗              "
		echo "            ║++:     . +  +   ..║++++.+║ .║+═╩═╗╔═╣╔╗║╔═╣║║+          .   "
		echo "            ║++:      ++══++   .║++ +++║ .║╚═╗ +║.+╚╝║+═╣╚╝+              "
		echo "           .║+++══*. ++++++++ ..║++  ++║  ╔═╝║ +║.*║║╠═╝║║║+              "
		echo "            ╚.****╝  :+    *:   ╚═.  ╚═:  +══╝.╚╝ ╚╝╚╩══╩╝╚╝              "
		echo "              .     .     .                   .     .   ...       ... .   "
		echo ""

		#preps
		bash install_packages.sh

		#run server
		bash run_server.sh
		;;

	"attach-server" ) bash run_client.sh;;

	"status" ) lsof -i :7070;;

	* )

		echo "                                          .                               "
		echo "                              . -#+ .    ##.                              "
		echo "                                :###=. ####                               "
		echo "                                  *###=. .    .                           "
		echo "                           %### ... *###=   =###                          "
		echo "                      .  .  .##- ###- +## +###*.   .                      "
		echo "                      .##...   ####  .  +###+.... ##@.                    "
		echo "                       @###. +### :##  ###+ ##+ .###                      "
		echo "                .  -     @###- .   ####.    +###+.  .   -.                "
		echo "                . #### ..  @###-. ...####. .. =###*. .###+                "
		echo "                   .#: ####..%#.+###.. #= ####  +#..####                  "
		echo "                   . ####.    =###+. .  ####.    .####.                   "
		echo "                 . #### .### *##= =##-.###..###. ### *##%                 "
		echo "                  ###.   .#### .   @###-.    ####.    =###                "
		echo "                      . :# -###=. #%.####. .#. ####  .                    "
		echo "                      .###%     ####     .####   ####                     "
		echo "                      ...     ####. .  .#### . .   +                      "
		echo "                            ####. ####.@## .###-                          "
		echo "                           *##  .  .####..  .###                          "
		echo "                                 .## -####..                              "
		echo "                               .####   -###.                              "
		echo ""
		echo "           .╔══╗.     . ══.     ╔═  . ═╗             .                    "
		echo "            ║++.     ..++++   ..║+++  +║  ╔++╦═+++╦══╦**╦╗╔╗              "
		echo "            ║++:     . +  +   ..║++++.+║ .║+═╩═╗╔═╣╔╗║╔═╣║║+          .   "
		echo "            ║++:      ++══++   .║++ +++║ .║╚═╗ +║.+╚╝║+═╣╚╝+              "
		echo "           .║+++══*. ++++++++ ..║++  ++║  ╔═╝║ +║.*║║╠═╝║║║+              "
		echo "            ╚.****╝  :+    *:   ╚═.  ╚═:  +══╝.╚╝ ╚╝╚╩══╩╝╚╝              "
		echo "              .     .     .                   .     .   ...       ... .   "
		;;

esac