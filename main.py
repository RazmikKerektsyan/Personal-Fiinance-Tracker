from finance_manager import FinanceManager

manager = FinanceManager()

while True:
    print("1. Add Income")
    print("2. Add Expense")
    print("3. Show Transactions Last Month")
    print("4. Delete Transaction")
    print("5. Set Limit")
    print("6. Show Monthly Budget")
    print("7. Check Monthly Budget")
    print("8. Exit")
    choice = input("აირჩიეთ მოქმედება: ").strip()
    if choice == "1":
        try:
            amount = float(input("შეიყვანეთ თანხა: ").strip())
            if amount <= 0:
                print("თანხა უნდა იყოს ნულზე მეტი")
                continue
            category = input("შეიყვანეთ კატეგორია: ").strip()
            date = input("შეიყვანეთ თარიღი (YYYY-MM-DD): ").strip()
            description = input("შეიყვანეთ აღწერა: ").strip()
            tx = manager.add_income(amount, category, date, description)
            print("შემოსავალი დაემატა! ID:", tx.id)
        except ValueError as error:
            print("შეცდომა:", error)
    elif choice == "2":
        try:
            amount = float(input("შეიყვანეთ თანხა: ").strip())
            if amount <= 0:
                print("თანხა უნდა იყოს ნულზე მეტი")
                continue
            category = input("შეიყვანეთ კატეგორია: ").strip()
            date = input("შეიყვანეთ თარიღი (YYYY-MM-DD): ").strip()
            description = input("შეიყვანეთ აღწერა: ").strip()
            tx = manager.add_expense(amount, category, date, description)
            print("ხარჯი დაემატა! ID: ", tx.id)
        except ValueError as error:
            print("შეცდომა:", error)
    elif choice == "3":
        try:
            month = input("შეიყვანეთ თვე(YYYY-MM): ").strip()
            tx_list = manager.get_transaction_month(month)
            if not tx_list:
                print("ამ თვეში ტრანზაქციები არ მოიძებნა!")
            else:
                for t in tx_list:
                    print(t)
        except ValueError as error:
            print("შეცდომა:", error)

    elif choice == "4":
        try:
            tx_id = int(input("შეიყვანეთ წასაშლელი ტრანზაქციის ID: ").strip())
            delete = manager.delete_transaction(tx_id)
            if delete:
                print("ტრანზაქცია წაიშალა!")
            else:
                print("ასეთი ID-ით ტრანზაქცია ვერ მოიძებნა!")
        except ValueError:
            print("შეცდომა: ID უნდა იყოს მთელი რიცხვი!")

    elif choice == "5":
        try:
            category = input("შეიყვანეთ კატეგორია: ").strip()
            limit = float(input("შეიყვანეთ ლიმიტი: ").strip())
            manager.set_budget(category, limit)
            print("ბიუჯეტის ლიმიტი განახლდა!")
        except ValueError as error:
            print("შეცდომა:", error)

    elif choice == "6":
        try:
            month = input("შეიყვანეთ თვე (YYYY-MM): ").strip()
            summary = manager.get_monthly_budget(month)
            print("ჯამური შემოსავალი:", summary["total_income"])
            print("ჯამური ხარჯი:", summary["total_expense"])
            print("ბალანსი:", summary["balance"])
        except ValueError as error:
            print("შეცდომა:", error)
    elif choice == "7":
        try:
            month = input("შეიყვანეთ თვე (YYYY-MM): ").strip()
            report = manager.check_budget(month)
            if not report:
                print("ბიუჯეტის კატეგორიები ჯერ არ არის დაყენებული!")
            else:
                for item in report:
                    print("კატეგორია:", item["category"])
                    print("დახარჯული:", item["spent"])
                    print("ლიმიტი:", item["limit"])
                    print("ლიმიტის გადაჭარბება:", item["exceeded"])
                    print("-" * 20)
        except ValueError as error:
            print("შეცდომა:", error)
    elif choice == "8":
        print("პროგრამა დასრულდა!")
        break
    else:
        print("არასწორი არჩევანი! სცადეთ თავიდან!")


