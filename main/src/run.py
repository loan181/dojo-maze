
# First parse user answer
try:
	# code.py is a file created with the user code
	from code import step
except ImportError as e:
	print("ERROR: La fonction step step() n'est pas définie")
	raise e
except Exception as e:
	print("ERROR:", str(e))
	raise e


# Test the code
import test

def main():
	try:
		filesName = (
			"easy1",
			"easy2",
			"easy3",

			"medium1",
			"medium2",
			"medium3",

			"hard1",
			"hard2",
			"hard3",
		)
		test.test(filesName)
	except Exception as e:
		print("ERROR:", e)

if __name__ == '__main__':
	main()
