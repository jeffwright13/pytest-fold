import pickle

def main():
    with open("test_reports_info_all.pickle", "rb") as f:
        test_reports_info_all = pickle.load(f)
        print("")

    with open("reports.pickle", "rb") as f:
        reports = pickle.load(f)
        print("")

    print("")

if __name__ == "__main__":
    main()
