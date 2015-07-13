# Web App Counter
Sinatra application reads from Redis pubsub channel and displays in flip board Solari style like train and airline boards. Display is from https://github.com/jayKayEss/Flapper . App is easily deployed at Heroku. 

System publishing to the channel is a Python app monitoring WiFi for client broadcasts. Used as a way to estimate # of WiFi devices in an area.

# Sniffer Client
Check out ./wifi_client_sniffer.py for the sniffer side. This script was run from Raspberry Pi with a airodump-ng compatible USB WiFi device. 
