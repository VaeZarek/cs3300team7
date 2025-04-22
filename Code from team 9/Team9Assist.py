this script:
jobApplicantList = []


def jobSeeker():
    skillsDone = False
    while skillsDone == False:
        userChoice = str(input("Enter your skills (enter q to quit): "))
        if (userChoice == "q"):
            break


def jobRecruiter():
    pass


def main():
    quitOut = False

    while quitOut == False:
        print("Select an option:")
        print("1. I am looking for a job")
        print("2. I am looking for an applicant")
        print("3. Quit\n")
        userChoice = int(input("Please select a number: "))

        match userChoice:
            case 1:
                jobSeeker()
            case 2:
                print("jobRecruiter()\n")
            case 3:
                print("Goodbye...")
                quitOut = True
            case _:
                print("Not a valid choice, please choose a valid number.")


if __name__ == '__main__':
    main()
