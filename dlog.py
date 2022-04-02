import sys
import re
from colorama import Fore, Back, Style

dialogue = []
choice_index = 1
choices = []
branches = []
vars = {}
user_response = ""

def reset():
	global choice_index, choices, branches, vars, user_response
	choice_index = 1
	choices = []
	branches = []
	user_response = ""

def getBranchIndex(branch_name):
	global dialogue
	return dialogue.index(f"#{branch_name}")

def process_dialogue(i):
	global dialogue, choice_index, choices, branches, vars, user_response

	if dialogue[i].startswith("##"):

		line = dialogue[i].split(" ", 2)

		user_response = input(": ").lstrip()

		if len(line) > 1 and line[1] == "=":
			var_name = line[2]
			vars[var_name] = user_response

		if user_response == "/exit":
			quit()
		elif len(branches) > 0:
			branch = branches[int(user_response)-1]
			process_dialogue(getBranchIndex(branch))

	elif dialogue[i].startswith("#"):
		reset()
		print()

	elif dialogue[i].startswith("\'"):
		line = dialogue[i].split(" ", 1)
		if len(line) <= 1:
			print()
		else:
			raw_text = line[1]
			text = raw_text
			while True:
				var_indices_list = [(m.start(0), m.end(0)) for m in re.finditer("(?<=\[).*?(?=\])", text)]
				if len(var_indices_list) == 0:
					break
				start_index, end_index = var_indices_list[0]
				var_name = text[start_index:end_index]
				var_value = vars[var_name] if var_name in vars else ""
				text = f'{text[:start_index-1]}{var_value}{text[end_index+1:]}'
			print(text)

	elif dialogue[i].startswith("@"):
		[choice_branch, choice_text] = dialogue[i].split(" ", 1)
		print(f'{choice_index}) {choice_text}')
		choices.append(choice_text)
		branches.append(choice_branch[1:])
		choice_index += 1

	elif dialogue[i].startswith(">"):
		branch = dialogue[i][1:]
		process_dialogue(getBranchIndex(branch))

	elif dialogue[i].startswith("var"):
		cmds = dialogue[i].split(" ")
		vars[cmds[1]] = cmds[3]
		print(vars)

	elif dialogue[i].startswith("--"):
		pass

	next_i = i + 1
	if next_i <= len(dialogue)-1: 
		process_dialogue(next_i)
	quit()

def clean_dialogue(dialogue):
	return [l for l in dialogue if l != ""]

def main():
	global dialogue

	file_name = sys.argv[1]

	with open(file_name, "r") as f:
		dialogue = clean_dialogue([line.rstrip() for line in list(f)])

	# Go through dialogue list

	process_dialogue(0)
			
if __name__ == "__main__":
    main()
