from discord_webhook import DiscordWebhook
import requests
import random
import string
import time
import os

class NitroGen: # Initialise the class
    def __init__(self): # The initaliseaiton function
        self.fileName = "Nitro Codes.txt" # Set the file name the codes are stored in
        self.proxies = [] # The list of proxies

    def main(self): # The main function contains the most important code
        os.system('cls' if os.name == 'nt' else 'clear') # Clear the screen

        print(""" █████╗ ███╗   ██╗ ██████╗ ███╗   ██╗██╗██╗  ██╗
██╔══██╗████╗  ██║██╔═══██╗████╗  ██║██║╚██╗██╔╝
███████║██╔██╗ ██║██║   ██║██╔██╗ ██║██║ ╚███╔╝
██╔══██║██║╚██╗██║██║   ██║██║╚██╗██║██║ ██╔██╗
██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║██║██╔╝ ██╗
╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝
                                                        """) # Print the title card
        time.sleep(2) # Wait a few seconds
        self.slowType("Made by: Drillenissen#4268 && Benz#4947", .02) # Print who developed the code
        time.sleep(1) # Wait a little more
        self.slowType("\nInput How Many Codes to Generate and Check: ", .02, newLine = False) # Print the first question
        num = int(input('')) # Ask the user for the amount of codes

        # Get the webhook url, if the user does not wish to use a webhook the message will be an empty string
        self.slowType("\nDo you wish to use a discord webhook? \nIf so type it here or press enter to ignore: ", .02, newLine = False)
        url = input('') # Get the awnser
        webhook = url if url != "" else None # If the url is empty make it be None insted

        self.slowType("\nWant to use proxies? (Y/n): ", .02, newLine = False) # Ask if they want to use a proxy
        proxy = input('') # Get the response

        if "y" in proxy.lower(): # If the awnser was yes to the question above
            self.proxySetup() # Trigger the proxy setup

        print() # Print a newline for looks

        valid = [] # Keep track of valid codes
        invalid = 0 # Keep track of how many invalid codes was detected

        if "y" in proxy.lower():
            total = 0
            proxyIndx = 0

            while total < num:
                try:
                    while total < num:
                        code = "".join(random.choices( # Generate the id for the gift
                            string.ascii_uppercase + string.digits + string.ascii_lowercase,
                            k = 16
                        ))
                        url = f"https://discord.gift/{code}" # Generate the url

                        result = self.quickProxyChecker(url, webhook, self.proxies[proxyIndx]) # Check the codes

                        if result == 200:
                            print(f" Valid | {url} | {result}")

                            if webhook is None:
                                total = num + 1

                        elif result == 429:
                            print(f" Ratelimited | {self.proxies[proxyIndx]}")
                            break
                        elif result == 404:
                            print(f" Invalid | {url} | {result}")
                except Exception as e:
                    self.slowType(f"Invalid Proxy | {self.proxies[proxyIndx]}")
                    self.proxies.remove(self.proxies[proxyIndx])

                proxyIndx += 1
                if proxyIndx == len(self.proxies):
                    proxyIndx = 0

        else:
            for i in range(num): # Loop over the amount of codes to check
                code = "".join(random.choices( # Generate the id for the gift
                    string.ascii_uppercase + string.digits + string.ascii_lowercase,
                    k = 16
                ))
                url = f"https://discord.gift/{code}" # Generate the url

                result = self.quickChecker(url, webhook) # Check the codes

                if result: # If the code was valid
                    valid.append(url) # Add that code to the list of found codes
                else: # If the code was not valid
                    invalid += 1 # Increase the invalid counter by one

                if result and webhook is None: # If the code was found and the webhook is not setup
                    break # End the script


        print(f"""
Results:
 Valid: {len(valid)}
 Invalid: {invalid}
 Valid Codes: {', '.join(valid )}""") # Give a report of the results of the check

        input("\nThe end! Press Enter 5 times to close the program.") # Tell the user the program finished
        [input(i) for i in range(4,0,-1)] # Wait for 4 enter presses


    def slowType(self, text, speed, newLine = True): # Function used to print text a little more fancier
        for i in text: # Loop over the message
            print(i, end = "", flush = True) # Print the one charecter, flush is used to force python to print the char
            time.sleep(speed) # Sleep a little before the next one
        if newLine: # Check if the newLine argument is set to True
            print() # Print a final newline to make it act more like a normal print statement

    def generator(self, amount): # Function used to generate and store nitro codes in a seperate file
        with open(self.fileName, "w", encoding="utf-8") as file: # Load up the file in write mode
            print("Wait, Generating for you") # Let the user know the code is generating the codes

            start = time.time() # Note the initaliseation time

            for i in range(amount): # Loop the amount of codes to generate
                code = "".join(random.choices(
                    string.ascii_uppercase + string.digits + string.ascii_lowercase,
                    k = 16
                )) # Generate the code id

                file.write(f"https://discord.gift/{code}\n") # Write the code

            # Tell the user its done generating and how long tome it took
            print(f"Genned {amount} codes | Time taken: {round(time.time() - start, 5)}s\n") #

    def fileChecker(self, notify = None): # Function used to check nitro codes from a file
        valid = [] # A list of the valid codes
        invalid = 0 # The amount of invalid codes detected
        with open(self.fileName, "r", encoding="utf-8") as file: # Open the file containing the nitro codes
            for line in file.readlines(): # Loop over each line in the file
                nitro = line.strip("\n") # Remove the newline at the end of the nitro code

                # Create the requests url for later use
                url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"

                response = requests.get(url) # Get the responce from the url

                if response.status_code == 200: # If the responce went through
                    print(f" Valid | {nitro} ") # Notify the user the code was valid
                    valid.append(nitro) # Append the nitro code the the list of valid codes

                    if notify is not None: # If a webhook has been added
                        DiscordWebhook( # Send the message to discord letting the user know there has been a valid nitro code
                            url = notify,
                            content = f"Valid Nito Code detected! @everyone \n{nitro}"
                        ).execute()
                    else: # If there has not been a discord webhook setup just stop the code
                        break # Stop the loop since a valid code was found

                else: # If the responce got ignored or is invalid ( such as a 404 or 405 )
                    print(f" Invalid | {nitro} ") # Tell the user it tested a code and it was invalid
                    invalid += 1 # Increase the invalid counter by one

        return {"valid" : valid, "invalid" : invalid} # Return a report of the results

    def quickChecker(self, nitro, notify = None): # Used to check a single code at a time
        # Generate the request url
        url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
        response = requests.get(url) # Get the response from discord
        print(response.status_code)

        if response.status_code == 200: # If the responce went through
            print(f" Valid | {nitro} ") # Notify the user the code was valid

            if notify is not None: # If a webhook has been added
                DiscordWebhook( # Send the message to discord letting the user know there has been a valid nitro code
                    url = notify,
                    content = f"Valid Nito Code detected! @everyone \n{nitro}"
                ).execute()

            return True # Tell the main function the code was found

        else: # If the responce got ignored or is invalid ( such as a 404 or 405 )
            print(f" Invalid | {nitro} ") # Tell the user it tested a code and it was invalid
            return False # Tell the main function there was not a code found

    def proxySetup(self):
        self.slowType("\nDo you want to use \n1: Pre generated proxies\n2: A standalone proxylist?\n(1,2): ", .02, newLine = False) # Ask for the proxy list
        awn = input('') # Get the awnser form the user

        if awn == "1":
            check = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=1500&ssl=yes").text
            responce = [i.strip() for i in check.strip().split("\n")]

        elif awn == "2":
            with open("proxy-list.txt", "w") as file:
                file.write("")

            self.slowType("\nPaste your list of proxies in the new file 'proxy-list.txt' where each proxy is on a new line, press enter once done", .02, newLine = False)
            input("")

            with open("proxy-list.txt", "r") as file:
                responce = [i.strip() for i in file.read().strip().split("\n")]

            os.remove("proxy-list.txt")

            # if len(responce) > 100:
            #     self.slowType("\nCannot accept more than 100 proxies at once", .02, newLine = False)
            #     exit()

        self.proxies = responce

        self.slowType(f"\nLoaded {len(responce)} preoxies", .02)

    def quickProxyChecker(self, nitro, notify = None, proxy = None): # Used to check a single code at a time
        # Generate the request url
        url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
        response = requests.get(url, {"https" : proxy}, timeout = 3) # Get the response from discord
        print(response.status_code)

        if response.status_code == 200: # If the responce went through
            print(f" Valid | {nitro} ") # Notify the user the code was valid

            if notify is not None: # If a webhook has been added
                DiscordWebhook( # Send the message to discord letting the user know there has been a valid nitro code
                    url = notify,
                    content = f"Valid Nito Code detected! @everyone \n{nitro}"
                ).execute()

        return response.status_code # Tell the main function the status code for checking for ratelimiting

if __name__ == '__main__':
    Gen = NitroGen() # Create the nitro generator object
    Gen.main() # Run the main code
