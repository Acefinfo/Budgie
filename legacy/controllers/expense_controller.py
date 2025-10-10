from sqlalchemy import func
from db.database import SessionLocal
from models.expense_db_model import Expense

from datetime import datetime


from views.expense_view import (
    show_expenses, show_summary, show_reports_menu,
    show_category_report, show_monthly_report,
    plot_category_pie, plot_monthly_trend,show_expense_menu)


def handle_add_expense():
    session = SessionLocal()
    try:
        while True:
            try:
                amount = float(input("Enter expense amount:"))
                if amount <= 0:
                    print("❌ Amount cannot be negative or zero.")
                    continue
                break
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")
        while True:
            category = input("Enter expense category:").strip().title()
            if len(category) < 1:
                print("❌ Category cannot be empty.")
            elif len(category) > 20:
                print("❌ Category too long (max 20 characters).")
            else:
                break
        dexcription = input("Enter the expense discription(Leave empty if no discription):").strip()
        expense = Expense(
            date=datetime.now().date(),
            amount=amount,
            category=category,
            description=dexcription
        )
        session.add(expense)
        session.commit()
        print("✅ Expense added successfully.")
    except Exception as e:
        session.rollback()
        print(f"❌ Failed to add expense: {e}")
    finally:
        session.close() 
        

def handle_view_expenses():
    session = SessionLocal()
    try:
        expenses = session.query(Expense).order_by(Expense.date.desc()).all()
        formatted_expenses = [
            {
                "id": exp.id,
                "date": exp.date.strftime("%Y-%m-%d"),
                "category": exp.category,
                "amount": exp.amount,
                "description": exp.description
            } for exp in expenses

        ]
        show_expenses(formatted_expenses)
    except Exception as e:
        print(f"❌ Failed to load expenses: {e}")
    finally:
        session.close()



def handle_summary():
    session = SessionLocal()
    try:
        result = session.query(
            func.sum(Expense.amount),
            func.min(Expense.amount),
            func.max(Expense.amount)
        ).one()
        total, lowest, highest = result
        show_summary(float(total or 0), float(lowest or 0), float(highest or 0))
    except Exception as e:
        print(f"❌ Failed to load summary: {e}")
    finally:
        session.close()
    


def handle_reports():
    session = SessionLocal()
    while True:
        try:
            choise = show_reports_menu()
            
            if choise == "1": # Category Report
                summary = session.query(
                    Expense.category, func.sum(Expense.amount)
                ).group_by(Expense.category).all()
                summary_dict = {cat:float(total) for cat, total in summary}
                show_category_report(summary_dict)
            
            elif choise == "2": # Monthly Report
                summary = session.query(
                    func.to_char(Expense.date, "YYYY-MM"),func.sum(Expense.amount)
                ).group_by(func.to_char(Expense.date, "YYYY-MM")).all()
                summary_dict = {month:float(total) for month, total in summary}
                show_monthly_report(summary_dict)  

            elif choise == "3": # Category pie chart 
                summary = session.query(
                    Expense.category, func.sum(Expense.amount)
                    ).group_by(Expense.category).all() 
                summary_dict = {cat:float(total) for cat, total in summary}
                plot_category_pie(summary_dict)

            elif choise == "4": # Monthly tend Chart
                summary = session.query(
                    func.to_char(Expense.date, "YYYY-MM"), func.sum(Expense.amount)
                    ).group_by(func.to_char(Expense.date, "YYYY-MM")
                    ).order_by(func.to_char(Expense.date, "YYYY-MM")).all()
                summary_dict = {month:float(total) for month, total in summary}
                plot_monthly_trend(summary_dict)
            
            elif choise == "5": # Back to main menu
                return  
            else:           
                print("❌ Invalid choice. Please try again.")

        except Exception as e: 
            print(f"❌ Failed to load reports: {e}")
        finally:
            session.close()

 
def handle_edit_expenses():
    session = SessionLocal()
    try:
        handle_view_expenses()
        try:
            expense_id = int(input("Enter the id of the expense you want to edit: "))
        except ValueError:
            print("❌ Invalid ID entered.")
            return
        
        expense = session.query(
            Expense
        ).filter(Expense.id == expense_id).first()

        if  not expense:
            print("Expense not found.")
            return

        new_amount = float(input("Enter new amount (leave blank to keep same amount as before): "))
        new_category = input("Enter new category (Leave blank to keep the same category as before): ").strip().title()
        new_discription = input("Enter new description (Leave blank to keep the same description as before):").strip()

        if new_amount:
            try:
                if new_amount <= 0:
                    print("❌ Amount muct be positive")
                    return
                expense.amount = new_amount
            except ValueError:
                print("❌ Invalid amount entered.")
                return
        
        if new_category:
            expense.category = new_category
        
        if new_discription:
            expense.description = new_discription
        
        session.commit()
        print("✅ Expense updated successfully.")

    except Exception as e:
        session.rollback()
        print(f"❌ Failed to update expense: {e}")
    finally:
        session.close()

def handle_delete_expenses():
    session = SessionLocal()
    try:
        handle_view_expenses()

        expense_id = input("Enter the ID of the expense you want to delete: ").strip()
        expense = session.query(
            Expense
        ).filter(Expense.id == expense_id).first()
        if not expense:
            print("❌ Expense not found.")
            return
        
        confirm = input(f"Are you sure you want to delete {expense}? (y/n) ").strip()
        if confirm.lower() in ["y", "yes"]:
            session.delete(expense)
            session.commit()
            print("✅ Expense deleted successfully.")
        else:
            print("❌ Deletion cancelled.")
    except Exception as e:
        session.rollback()
        print(f"❌ Error in deleting expense: {e}")
    finally:
        session.close()

    