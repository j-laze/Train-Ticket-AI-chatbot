# from transformers import GPT2LMHeadModel, GPT2Tokenizer
#
#
# class RuleBasedBot:
#     def __init__(self):
#         self.rules = {
#             "buy a ticket": ["departure station", "destination station", "date"],
#             # Add more rules as needed
#         }
#         self.user_info = {}
#         self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
#         self.model = GPT2LMHeadModel.from_pretrained("gpt2")
#
#     def respond(self, user_input):
#         user_input = user_input.lower()  # Convert the user input to lower case
#         if user_input in self.rules:
#             self.user_info[user_input] = []
#             return self.ask_for_info(user_input)
#         else:
#             return self.generate_response(user_input)
#
#     def ask_for_info(self, user_input):
#         for info in self.rules[user_input]:
#             if info not in self.user_info[user_input]:
#                 return self.generate_response(f"Could you please provide the {info}?")
#         return self.generate_response("Thank you for providing all the required information.")
#
#     def update_info(self, user_input, info):
#         if user_input in self.user_info:
#             self.user_info[user_input].append(info)
#
#     def generate_response(self, prompt):
#         inputs = self.tokenizer.encode(prompt, return_tensors='pt')
#         outputs = self.model.generate(inputs, max_length=100, temperature=0.7)
#         response = self.tokenizer.decode(outputs[0])
#         return response
#
#
# bot = RuleBasedBot()
#
# while True:
#     user_input = input("User: ")
#     if user_input.lower() == "quit":
#         break
#     response = bot.respond(user_input)
#     print("Bot: ", response)
# # Outputs: "Could you please provide the destination station?"