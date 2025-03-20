from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
import sqlite3
import csv
from datetime import datetime
import pandas as pd
import logging
import os



class ActionProvideProductInfo(Action):

    def name(self) -> Text:
        return "action_provide_product_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        product_info = (
            "Here are the products we offer\n"
            "1. Online TV plan\n"
            "2. Data Plan\n"
            "3. On Demand Movie Streaming\n"
            "4. PPV\n"
            "5. Online Video Games\n"
            "6. Home Security\n"
            "7. Utilities\n"
            "\n"
            "For more details, please respond with the number of the product you're interested in."
        )
        dispatcher.utter_message(text=product_info)

        return []


class ActionProvideDetailedProductInfo(Action):

    def name(self) -> Text:
        return "action_provide_detailed_product_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_response = tracker.latest_message.get('text')
        detailed_info = "Thank you for your response. Here is some additional information:\n\n"

        if user_response == "1":
            detailed_info += (
                "Online TV plan:\n"
                "   - Basic: 50 channels\n"
                "   - BasicPlus: 100 channels\n"
                "   - Ultimate: 200 channels"
            )
        elif user_response == "2":
            detailed_info += (
                "Data Plan:\n"
                "   - WiFi SpeedLane: 100/5 Mbps speed\n"
                "   - WiFi LightLane: 250/30 Mbps speed"
            )
        elif user_response == "3":
            detailed_info += (
                "On Demand Movie Streaming:\n"
                "   - Premium: 100 movies a month\n"
                "   - Ultimate: 500 movies a month"
            )
        elif user_response == "4":
            detailed_info += (
                "PPV:\n"
                "   - Live Sports Events\n"
                "   - PPV Movies"
            )
        elif user_response == "5":
            detailed_info += (
                "Online Video Games:\n"
                "   - Premium: 100 games a month\n"
                "   - Ultimate: 200 games a month"
            )
        elif user_response == "6":
            detailed_info += (
                "Home Security:\n"
                "   - Security Cameras and Alarms\n"
                "   - Remotely Unlock/Lock main entrance"
            )
        elif user_response == "7":
            detailed_info += (
                "Utilities:\n"
                "   - Lighting: Remotely control house lights\n"
                "   - Thermostat: Remotely control the house thermostat"
            )
        else:
            detailed_info = "I'm sorry, I didn't understand that. Please respond with a number between 1 and 7."

        dispatcher.utter_message(text=detailed_info)
        dispatcher.utter_message(text="Which plan would you like to purchase today?")
        return []


class ActionCreateOrder(Action):
    def name(self) -> Text:
        return "action_create_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        customer_name = tracker.get_slot("customer_name")
        product_name = tracker.get_slot("product")
        product_plan = tracker.get_slot("plan")
        credit_card = tracker.get_slot("credit_card_number")

        # Save order information to a CSV file
        order_data = {
            "customer_name": customer_name,
            "product_name": product_name,
            "product_plan": product_plan,
            "order_date": datetime.now().strftime("%Y-%m-%d"),
            "credit_card": credit_card
        }

        order_data_df = pd.DataFrame([order_data])
        
        dfOrig = pd.read_csv('customer_orders.csv')
        
        udpatedDF = pd.concat([dfOrig, order_data_df], ignore_index=True)

        udpatedDF.to_csv('customer_orders.csv', index=False)
    
        return [AllSlotsReset()]




class ActionScheduleIncidentTicket(Action):

    def name(self) -> Text:
        return "action_schedule_incident_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        customer_name = tracker.get_slot("customer_name")
        issue_description = tracker.get_slot("issue_description")
        ticket_status = "Open"
        assigned_technician = "Unasigned"
        creation_date = datetime.now().strftime("%Y-%m-%d")
        resolution_date = ""

        # Write customer information to the CSV file using pandas
        incident_ticket_data = {
            "customer_name": customer_name,
            "issue_description": issue_description,
            "ticket_status": ticket_status,
            "assigned_technician": assigned_technician,
            "creation_date": creation_date,
            "resolution_date": resolution_date
        }


        incident_ticket_df = pd.DataFrame([incident_ticket_data])
        
        dfOrig = pd.read_csv('incident_tickets.csv')
        
        udpatedDF = pd.concat([dfOrig, incident_ticket_df], ignore_index=True)

        udpatedDF.to_csv('incident_tickets.csv', index=False)


        return [AllSlotsReset()]



class ActionAssignSpecialistToTicket(Action):

    def name(self) -> Text:
        return "action_assign_specialist_to_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        specialist_name = tracker.get_slot("specialist")

        # Read the incident tickets from the CSV file
        df = pd.read_csv('incident_tickets.csv')

        # Update the tickets that are "Unnasigned" with the specialist name
        df.loc[df['assigned_technician'] == "Unasigned", 'assigned_technician'] = specialist_name

        # Save the updated DataFrame back to the CSV file
        df.to_csv('incident_tickets.csv', index=False)

        dispatcher.utter_message(text=f"All unassigned tickets have been assigned to {specialist_name}.")
        return [AllSlotsReset()]

class ActionUpdateTicketStatus(Action):

    def name(self) -> Text:
        return "action_update_ticket_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ticket_status = tracker.get_slot("ticket_status")
        customer_name = tracker.get_slot("customer_name")

        # Read the incident tickets from the CSV file
        df = pd.read_csv('incident_tickets.csv')

        # Update the ticket status for the specified customer
        df.loc[df['customer_name'].str.contains(customer_name, case=False, na=False), 'ticket_status'] = ticket_status

        # Save the updated DataFrame back to the CSV file
        df.to_csv('incident_tickets.csv', index=False)

        dispatcher.utter_message(text=f"The ticket status for {customer_name} has been updated to {ticket_status}.")
        return [AllSlotsReset()]
    
class ActionCreateCustomerAccount(Action):
    def name(self) -> Text:
        return "action_create_customer_account"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        customer_name = tracker.get_slot("customer_name")
        email = tracker.get_slot("email")
        phone = tracker.get_slot("phone")
        datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save customer information to a CSV file
        customer_data = {
            "customer_name": customer_name,
            "email": email,
            "phone": phone,
            "creation_date": datetime_now
        }

        customer_data_df = pd.DataFrame([customer_data])
        
        dfOrig = pd.read_csv('customer_accounts.csv')
        
        udpatedDF = pd.concat([dfOrig, customer_data_df], ignore_index=True)

        udpatedDF.to_csv('customer_accounts.csv', index=False)
    
        return []
    

class ActionCancelOrder(Action):

    def name(self) -> Text:
        return "action_cancel_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        customer_name = tracker.get_slot("order_name")

        # Read the incident tickets from the CSV file
        df = pd.read_csv('customer_orders.csv')

        # Update the ticket status for the specified customer
        df.loc[df['customer_name'].str.contains(customer_name, case=False, na=False), 'status'] = "Cancel"

        # Save the updated DataFrame back to the CSV file
        df.to_csv('customer_orders.csv', index=False)

        return []
    

class ActionCheckOrderStatus(Action):
    def name(self) -> Text:
        return "action_check_order_status"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        order_number = tracker.get_slot("order_number")

        # Read the customer orders from the CSV file
        df = pd.read_csv('customer_orders.csv')

        try:
            order_number = int(order_number)
            if order_number < 1 or order_number > len(df):
                dispatcher.utter_message(text=f"Order number {order_number} does not exist.")
            else:
                order_info = df.iloc[order_number - 1].to_dict()
                dispatcher.utter_message(text=f"Order details for order number {order_number}: {order_info}")
        except ValueError:
            dispatcher.utter_message(text="Invalid order number. Please provide a valid number.")

            return [AllSlotsReset()]
    
