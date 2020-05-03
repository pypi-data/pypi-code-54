string = "call( a , b )"

label, rest = string.split(":")
label = label.strip()
rest = rest.replace(" ", "")

print(label + ":" + rest)
