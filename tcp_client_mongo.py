import socket
import json


class TCPclient():
    def __init__(self, sms):
        self.target_ip = 'localhost'
        self.target_port = 9997
        self.input_checking(sms)

    def client_runner(self):

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))

        # client.send(self.client_sms)
        #
        #     received_from_server = client.recv(4096)
        #
        #     recv_sms = received_from_server.decode("utf-8")
        #
        #     print("$:", recv_sms)
        #
        #     client.close()
        return client  # to send and received data

    def input_checking(self, sms):
        if sms == "gad":
            self.get_all_data(sms)

        elif sms == "login":
            self.login(sms)

        elif sms == "reg":
            self.register()
        else:
            print("Invalid Option")

    def get_all_data(self, sms):
        client = self.client_runner()
        sms = bytes(sms + ' ', "utf-8")
        client.send(sms)
        received_from_server = client.recv(4096)
        # print(received_from_server.decode("utf-8"))

        dict_data: dict = json.loads(received_from_server.decode("utf-8"))
        print(type(dict_data))
        print(dict_data)
        client.close()

    def login(self, info):
        try:
            print("This is login Form")
            l_email = input("Enter your email to login:")
            l_pass = input("Enter your password to login:")

            client = self.client_runner()
            sms = info + ' ' + l_email + ' ' + l_pass  # login email password
            sms = bytes(sms,"utf-8")
            client.send(sms)
            received_from_server = client.recv(4096)
            user_info: dict = json.loads(received_from_server.decode("utf-8"))
            self.option_choice(user_info, client)
            client.close()


        except Exception as err:
            print(err)

    def option_choice(self, user_info, client):
        print("Email :", user_info["email"])
        print("Info :", user_info["info"])
        print("Point :", user_info["point"])

        try:
            option = input("Press 1 to Get User Option:\nPress 2 To Get Main Option:\nPress 3 To Exit:")
            if option == '1':
                self.user_option(user_info, client)
            elif option == '2':
                self.input_checking("from_option")  # to write more option
            elif option == '3':
                exit(1)
            else:
                print("Invalid Option [X]")
                self.option_choice(user_info, client)

        except Exception as err:
            print(err)

    def user_option(self, user_info, client):
        try:
            option = input("    ***###****\nPress 1 To Vote:\nPress 2 to get more points:\nPress 3 to Transfer Point:\n"
                           "Press 4 To get Voting Ranking:\nPress 5 to change user information \nPress 6 to Delete Acc:\nPress 7 "
                           "to Exit:")

            if option == '1':
                self.votingSection(user_info,client)
            elif option == '2':
                self.transfer_point(user_info,client)
            elif option == '3':
                self.transfer_point(user_info,client)
            else:
                print("Invalid option")
                self.user_option(user_info, client)

        except Exception as err:
            print(err)
            self.user_option(user_info, client)

#voting Section
    def votingSection(self, user_info, client):
        client = self.client_runner()
        sms = bytes("candidate_info", "utf-8")
        client.send(sms)

        info = client.recv(4096)
        candi_info = json.loads(info.decode("utf-8"))
        # print(candi_info)
        # print(type(candi_info))
        print("1 vote for 10 points")
        for i in candi_info:
            print("No: ", i, "Name: ", candi_info[i]["name"], "vote", candi_info[i]["vote_point"])
        client.close()
        self.selec_candidate(candi_info,user_info, client)

#Select candidate Section
    def selec_candidate(self,candi_info,user_info, client):
        try:
            candidate = input("Choose number your canditate to vote type no to cancel")
            if candidate == "no":
                self.user_option(user_info, client)
            for i in candi_info:
                if candidate == i:
                    vote = candi_info[i]["vote_point"] + 1
                    vote_form = "vote" + " " + candi_info[i]["name"] + " " + str(vote)
                    
                    client = self.client_runner()
                    client.send(bytes(vote_form, "utf-8"))
                    
                    received_from_server = client.recv(4096)
                    candi_info: dict = json.loads(received_from_server.decode("utf-8"))
                    client.close()
                    for i in candi_info:
                        print("No: ", i, "Name: ", candi_info[i]["name"], "vote", candi_info[i]["vote_point"])
                    client.close()
                    self.selec_candidate(candi_info,user_info, client)
                    break
                else:
                    print("Plz enter a valid Cadidate number")
                    self.selec_candidate(candi_info,user_info, client)
        except Exception as err:
            print("select candidate ! error plz select a valid canditate ..")
            self.selec_candidate(candi_info,user_info, client)

#Transfer Points 
    def transfer_point(self,user_info,client):
            print("your point Point :", user_info["point"])
            userPoint = int(user_info["point"])
            if int(user_info["point"]) != 0:
                try:
                    point = int(input("Enter your pioint to transfer"))
                    if  point <= userPoint:
                        trans_user:dict =  self.transferUser(point)
                        tranUserPoint =int(trans_user["point"])
                    
                        
                        tranUserPoint = tranUserPoint + point
                        userPoint = userPoint - point

                        data_form = "update_point" + " " + trans_user["email"] + " " + str(tranUserPoint) + " " + user_info["email"] + " " + str(userPoint)
                        
                        client = self.client_runner()
                        client.send(bytes(data_form, "utf-8"))
                        
                        received_from_server = client.recv(4096)
                        user_info: dict = json.loads(received_from_server.decode("utf-8"))
                        print(user_info)
                        self.option_choice(user_info, client)
                        client.close()

                    else:
                        print("U have unsficient point to transfer ...")
                        self.transfer_point(user_info,client)

                except Exception as error:
                    print(error,"invalid transfer plz try again")
                    self.transfer_point(user_info,client)
            else:
                print("You have unsuficinent amount pint to transfer!")
                self.transfer_point(user_info,client)

#transfer user Checking validation
    def transferUser(self,point):
            info = "transfer_email"
            try:
                email = input("Enter your transfer email :")
                client = self.client_runner()
                sms = info + ' ' + email 
                sms = bytes(sms,"utf-8")
                client.send(sms)

                received_from_server = client.recv(4096)
                user_info = json.loads(received_from_server.decode("utf-8"))
                print(user_info)
                if email ==  user_info["email"]:
                    return user_info
                else:
                    print("invalid transfer user")
                    self.transferUser(point)
            except Exception as err:
                print(err)
                self.transferUser(point)


    def register(self):
        print("\nThis is registration option ")
        r_email = ''
        while True:
            r_email = input("Enter email for registration :")
            flag = self.email_checking(r_email)  # 1 or -1

            if flag == 1:
                break
            else:
                print("Email Form Invalid\nTry Again! ")

        print("Email From Valid ")

        try:
            option = input("Press 1 Registration for Voter:\nPress 2 Registration for Candidate!:")

            if option == '1':
                self.reg_for_voter(r_email)
            elif option == '2':
                self.reg_for_candidate(r_email)

            else:
                self.register()
        except Exception as err:
            print(err)

    def email_checking(self, r_email):
        name_counter = 0
        for i in range(len(r_email)):
            if r_email[i] == '@':
                # print("Name End Here")
                break
            name_counter += 1

        print("Name counter: ", name_counter)

        email_name = r_email[0:name_counter]
        email_form = r_email[name_counter:]

        # print(email_name)
        print(email_form)

        # checking for name
        name_flag = 0
        email_flag = 0
        for i in range(len(email_name)):
            aChar = email_name[i]
            if (ord(aChar) > 31 and ord(aChar) < 48) or (ord(aChar) > 57 and ord(aChar) < 65) or (
                    ord(aChar) > 90 and ord(aChar) < 97) or (ord(aChar) > 122 and ord(aChar) < 128):
                name_flag = -1
                break

        domain_form = ["@facebook.com", "@ncc.com", "@mail.ru", "@yahoo.com", "@outlook.com", "@apple.com", "@zoho.com",
                       "@gmail.com"]

        for i in range(len(domain_form)):

            if domain_form[i] == email_form:
                email_flag = 1
                break

        if name_flag == -1 or email_flag == 0:
            return -1

        else:
            return 1
        
#Register voter
    def reg_for_voter(self, r_email):

        if self.email_check_inDB(r_email):
            try:
                username = input("Enter your voter username :")
                pass1 = input("Enter your password to register:")
                pass2 = input("Enter your password Again  to register:")

                if pass1 == pass2:
                
                    print("Password Was match!")
                    phone = int(input("Enter your phone number:"))

                    data_list = [username,r_email, pass1, phone]
                    print(data_list)
                    self.final_registration(data_list,"voter")

                else:
                    print("Password not match:")
                    self.reg_for_voter(r_email)


            except Exception as err:
                print(err)

        else:

            print("Your email was already register!")
            self.register()

#register candidate
    def reg_for_candidate(self, r_email):

        if self.email_check_inDB(r_email):
            try:
                username = input("Enter your Candidate username :")
                pass1 = input("Enter your password to register :")
                pass2 = input("Enter your password Again  to register:")

                if pass1 == pass2:

                    print("Password Was match!")
                    phone = int(input("Enter your phone number:"))

                    data_list = [username,r_email, pass1, phone]
                    self.final_registration(data_list,"canditate")

                else:
                    print("Password not match:")
                    self.reg_for_candidate(r_email)


            except Exception as err:
                print(err)

        else:

            print("Your email was already register!")
            self.register()

    def email_check_inDB(self, email):

        client = self.client_runner()
        data = "emailcheck" + " " + email

        client.send(bytes(data, "utf-8"))

        received = client.recv(4096).decode("utf-8")

        print(received)

        if received == "notExist":
            client.close()
            return True
        else:
            client.close()
            return False

    def final_registration(self, data_list,userdata):
        if userdata == "canditate":
            data_form = "candidate_register" + " " + data_list[0] + " " + data_list[1] + " " + data_list[2] + " " + str(data_list[3]) + " " + "User_"+data_list[0] + " " + "0"
            print(data_form)
        else:
            data_form = "voter_register" + " " + data_list[1] + " " + data_list[2] + " " + str(data_list[3]) + " " + "User_"+data_list[0] + " " + "100"

        client = self.client_runner()

        client.send(bytes(data_form, "utf-8"))

        recv = client.recv(4096).decode("utf-8")

        print(recv)

        if recv:
            print("Registration Success!",recv)
            info="login"
            self.login(info)

        client.close()

    


if __name__ == "__main__":
    while True:
        sms = input("Enter some data to send:")
        tcp_client = TCPclient(sms)