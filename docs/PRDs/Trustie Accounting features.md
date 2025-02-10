

# Types of Transfers

- Internal Transfer = Net - Zero = matching incoming and outgoing transactions.

- Incoming -Transfer.  Treasted as regular credit i.e income, in either the recurrring or non-recurring as appropriates. Won't appear in spend pockets. Do not include in the mood categories.  

- Outgoing Transfer:  Manually tag the Category for outgoing. Prior to Taggig, is mapped to Unclassifed "Tag Me" .  IN the spending pockets show the outgoing Transfers as uncategorised. 

# Money Moods
[[
]]Tag only the debit transactdions. 


![[./Pasted image 20250208093446.png]]




**1. Screen Name & Purpose**

• **Screen Name:** Money Moods

• **Purpose:** Encourages users to **manually categorize each transaction** into one of **four Money Moods** to build mindful spending habits.

• **User Benefit:**

• Encourages **daily spending reflection** for **better financial control** and **less stress**.

• Shifts the focus from just “how much was spent” to “how it made me feel.”

• Helps users identify trends in their spending behavior over time.

**2. Key Features & Functionality**

  

**A. Displayed Information**

1. **Money Mood Breakdown (Pie Chart)**
No postitive (credit) transactions in the Money Moods. 

• **Visual representation** of how the user categorized their spending for the selected month.

• Each slice represents a **Money Mood category**, proportionate to total spending.

- Should always represent the Current Month

- Should not display Net-
• **Unclassified (Tag Me) transactions** are shown separately to encourage users to complete their categorization.

2. **Money Mood Categories & Business Logic**

• **Users manually tag each debit transaction** into one of the following categories:

|**Mood**|**Description**|**Emoji**|**Example Transactions**|
|---|---|---|---|
|**Needs**|Essential expenses|🏡|Rent, bills, groceries|
|**Wants**|Non-essential but desirable|🛍️|Shopping, dining out|
|**Saving / For Future You**|Money set aside for future goals|🐖|Savings, investments|
|**Joy**|Purchases that genuinely enhance happiness|🎉|Gifts, experiences|
|**Tag Me (Unclassified)**|Uncategorized transactions|🤔|Pending categorization|

Savings are identifies as follows
- Manually Tagged by the user
- Remembered by app. (match description / destination)
- (How to treat a positive balance between monthly income and outgoings, Add app feature to suggest to move to savings account or investment account).  
- For the moment we will treat positive balance at the end of the month as Saving.  

[  ]  Add more explainatory stuff.  


1. **Connect & Inspire Section**

• Users can share their **Money Mood insights** with friends **without showing actual amounts** (only % breakdown).

• Encourages financial transparency in a **non-judgmental, positive way.**

**3. Data Requirements & Calculation Logic**

  

**A. Data Fields Required**

|**Field**|**Description**|**Source**|
|---|---|---|
|transactions[]|List of debit transactions for the month|Bank API (Saltedge)|
|category|User-assigned Money Mood category|Trustie App (User Input)|
|amount|Transaction value|Bank API|
|total_spent|Sum of all categorized transactions|Computed Value|

**B. Calculation Logic for Pie Chart Slices**

  

Each category’s percentage is calculated as:

• **Example Calculation (from the provided screenshot):**

```
Total Spent: £19,582
Total Savings: £16,874
Saving % = (16,874 ÷ 19,582) × 100 = ~86%
Tag Me (Unclassified) % = (2,708 ÷ 19,582) × 100 = ~14%
```

  

• **Edge Case Handling:**

• If some transactions are **unclassified**, the **Tag Me** section appears larger, prompting users to complete their tagging.

• If **all transactions are categorized**, the **Tag Me** category is hidden.

**4. Error Handling & Edge Cases**

|**Scenario**|**Expected Behavior**|
|---|---|
|No transactions for the month|Display “No spending recorded yet”|
|No categorized transactions|Display prompt: “Tag your spending to see your Money Moods”|
|Transactions missing categories|Show “Tag Me” slice in pie chart with a CTA to categorize|
|API failure fetching transactions|Show error message: “Unable to load spending data. Try again.”|

**5. UI/UX Behavior**

• **Loading State:** Show a skeleton UI while transactions are being fetched.

• **Animations:** Smooth pie chart transitions when new categories are added.

• **Color Coding:**

• **Each Money Mood has a unique color** (e.g., green for savings, blue for needs, pink for joy).

• **Tag Me (Unclassified) appears in dark gray** to prompt action.

• **Interactive Elements:**

• Tapping on a pie chart section filters transactions by that mood.

• Tapping “Tag Me” opens the categorization screen.

**6. Success Criteria & Testing Guidelines**

  

✅ Users can **manually tag** each transaction into one of the four categories.

✅ The **pie chart updates dynamically** as transactions are tagged.

✅ Unclassified transactions are **correctly assigned to “Tag Me”** until categorized.

✅ The **percentage calculations match the transaction breakdown**.

✅ Users can **share their Money Moods** without revealing transaction amounts.

**7. Analytics & Tracking**

• **Event: money_moods_viewed** → When the screen is opened.

• **Event: transaction_tagged** → When a user categorizes a transaction.

• **Event: money_moods_shared** → When a user shares their breakdown.

• **Event: all_transactions_tagged** → When the user completes all categorizations.

**Next Steps**

  



✅  **automated suggestions** (e.g., auto-tagging based on past behavior)?

  





# Accounts Overview


![[Pasted image 20250208091804.png]]



  

• **Purpose:** Displays a summary of the user’s **linked bank accounts**, their balances, and a total balance across all accounts. Allows users to **link a new bank account**.



**2. Key Features & Functionality**

Refresh 4 times per day.
Callback.



**A. Displayed Information**

• **Total Balance** (Large Red Text): Sum of all linked account balances.

• **List of Linked Accounts**:

• **Bank Name & Logo** (e.g., NatWest, PayPal).

• **Masked Account Number** (First 6 + Last 4 digits shown for security).

• **Account Balance** (Formatted as currency).

  

**B. Actions & Interactions**

2. **Link Bank Account Button (+ Icon)**

• **Action:** Opens a flow to link a new bank account via Open Banking (Saltedge API).

• **Expected Behavior:** Redirects the user to the Saltedge authentication screen.

• **Edge Cases:**

• If linking fails, show error message (“Failed to connect. Please try again.”).

• If a duplicate account is detected, show a warning.

3. **Tapping an Account**

• **Action:** Expands the account details or navigates to a “Transactions” screen.

• **Expected Behavior:** Shows **recent transactions** for that account.

**3. Data Requirements & API Calls**

  

**A. Data Fields Required**

• account_name (e.g., “NatWest”)

• account_number_masked (e.g., “60-04-23 ••••3216”)

• balance (e.g., “£30”)

• account_logo_url (Bank logo from API)

  

**B. API Endpoints Used**

4. **Fetch Linked Accounts (GET /accounts)**

• **Purpose:** Retrieves all user-linked accounts and balances.

• **Response Example:**

```
{
  "accounts": [
    { "bank": "NatWest", "account_number": "60-04-23 22903216", "balance": 30, "currency": "GBP" },
    { "bank": "NatWest", "account_number": "60-04-23 22993673", "balance": 1013, "currency": "GBP" },
    { "bank": "PayPal", "account_number": "••••", "balance": 37, "currency": "GBP" }
  ],
  "total_balance": 1081
}
```

  

5. **Link New Account (POST /accounts/link)**

• **Purpose:** Initiates the Open Banking linking process.

• **Response Example:**

```
{ "status": "pending", "redirect_url": "https://saltedge.com/auth" }
```

**4. Error Handling & Edge Cases**

| **Scenario**                | **Expected Behavior**                                     |
| --------------------------- | --------------------------------------------------------- |
| API fails to fetch accounts | Show error message: “Unable to load accounts. Try again.” |
| Account balance is null     | Show £0 with warning: “Balance unavailable”               |
| No accounts linked          | Display “No linked accounts. Tap + to add one.”           |
| Linking a duplicate account | Show: “This account is already linked.”                   |

**5. UI/UX Behavior**

• **Loading State:** Show a loading animation (skeleton UI) while fetching accounts.

• **Error States:** If an error occurs, show a **retry button**.

• **Dark Mode Support:** Ensure text colors are visible against the background.

**6. Success Criteria & Testing Guidelines**

  

✅ Users can see all linked accounts with correct balances.

✅ Users can tap an account to navigate to transactions.

✅ Users can link a new account and complete authentication via Open Banking.

✅ API errors are handled gracefully with appropriate messages.

✅ UI remains responsive on different screen sizes.

**7. Analytics & Tracking**

• **Event: account_link_attempted** → When a user taps “Link Bank Account”.

• **Event: account_link_success** → When a new account is successfully linked.

• **Event: account_link_failed** → When an error occurs during linking.

• **Event: account_viewed** → When a user lands on this screen.


### Next steps
✅  Add indication of how old the last refresh is ... 
add manual refresh.  
- Saltedge has 3 native fields specify which one is displayed.  ) Name, Nature, Provide Card, 
- Display the "Name" 
- Add account Nick names
- Need ability to classify account as Current | Savings |  
- Possibly via the long press on the account name 
- Adding Nudges to Create High Yield Savings Accounts (HYSA) etc
- 




# Saving Look ahead

**1. Screen Name & Purpose**

• **Screen Name:** Saving Look Ahead

• **Purpose:** Provides an **overview of expected financial flow for the current month**, displaying **total income (“In”), total spending (“Out”), and net savings (“Saved”)**.

• **User Benefit:** Helps users **anticipate their cash flow**, track progress, and make informed financial decisions.

**2. Key Features & Functionality**

  

**A. Displayed Information**

6. **In (Total Income for the Month)**

• Represents **all money expected to come in during the current month**.


• **Includes:**

• Salary deposits

• Side hustle earnings

• Refunds, cash gifts, or one-time deposits


• **Displayed Format:** "£X,XXX" (positive value, formatted in red).

7. **Out (Total Spend So Far)**

• Represents **all expenses incurred so far this month**.

• **Includes:**
- Spend to date plus 
- All the future Recurring Transactions 
- 
• Card transactions

• Direct debits & standing orders

• ATM withdrawals

• Subscription payments

• **Displayed Format:** "-£X,XXX" (negative value, formatted in red).

8. **Saved (Net Savings So Far)**

• Represents **total income minus total spending** (i.e., net cash flow).

• **Calculation Formula:**

• **Displayed Format:**

• If positive: "£X,XXX" (indicating a surplus).

• If negative: "-£X,XXX" (indicating overspending).

**3. Data Requirements & Calculation Logic**

  

**A. Data Fields Required**

|**Field**|**Description**|**Source**|
|---|---|---|
|income_transactions[]|List of all income transactions for the month|Bank API (Saltedge)|
|expense_transactions[]|List of all expense transactions for the month|Bank API (Saltedge)|
|forecasted_income[]|Recurring salary, freelance income, etc.|User-defined or AI-predicted|
|forecasted_expenses[]|Expected expenses (e.g., rent, subscriptions)|User-defined or AI-predicted|
|net_savings|total_income - total_expense|Computed value|

**B. API Endpoints Used**

9. **Fetch Income Transactions (GET /transactions?type=income&date=current_month)**

• Returns a list of all **income transactions** for the current month.

• **Response Example:**

```
{
  "transactions": [
    { "source": "Salary", "amount": 16000, "date": "2024-02-01" },
    { "source": "Freelance", "amount": 500, "date": "2024-02-10" },
    { "source": "PayPal Refund", "amount": 374, "date": "2024-02-15" }
  ],
  "total_income": 16874
}
```

  

• **Calculation for “In” Value:**

```
in_total = sum(transaction["amount"] for transaction in income_transactions)
```

  

10. **Fetch Expense Transactions (GET /transactions?type=expense&date=current_month)**

• Returns a list of **all spending transactions** for the current month.

• **Response Example:**

```
{
  "transactions": [
    { "category": "Rent", "amount": -1000, "date": "2024-02-01" },
    { "category": "Groceries", "amount": -200, "date": "2024-02-05" },
    { "category": "Entertainment", "amount": -500, "date": "2024-02-10" },
    { "category": "Utilities", "amount": -120, "date": "2024-02-15" },
    { "category": "Shopping", "amount": -780, "date": "2024-02-18" }
  ],
  "total_expense": -19582
}
```

  

• **Calculation for “Out” Value:**

```
out_total = sum(transaction["amount"] for transaction in expense_transactions)
```

  

11. **Compute Net Savings (Saved Value)**

• **Formula:**

```
saved_total = in_total - abs(out_total)
```

  

• **Example Calculation for Provided Screenshot:**

```
In: £16,874
Out: -£19,582
Saved: 16,874 - 19,582 = -£2,708
```

**4. Error Handling & Edge Cases**

|**Scenario**|**Expected Behavior**|
|---|---|
|API fails to fetch income/expense data|Show “Data unavailable” with retry button|
|No income transactions this month|Display “No income recorded yet”|
|No expense transactions this month|Display “No spending recorded yet”|
|Net savings is negative|Display savings value in red with warning: “You’ve spent more than you earned”|
|Missing or incorrect currency format|Default to GBP (£) and round values|

**5. UI/UX Behavior**

• **Loading State:** Show skeleton UI while fetching data.

• **Animations:** Smooth number transitions when data updates.

• **Color Coding:**

• **Income (“In”)** → Always **red**.

• **Expenses (“Out”)** → Always **red**.

• **Savings (“Saved”)** → **Red if negative**, **green if positive**.

**6. Success Criteria & Testing Guidelines**

  

✅ **Income and expense values correctly fetched from API**.

✅ **Net savings calculation (Saved = In - Out) is accurate**.

✅ **Handles API failures and missing data gracefully**.

✅ **UI updates dynamically when transactions are added**.

**7. Analytics & Tracking**

• **Event: savings_lookahead_viewed** → When the screen is opened.

• **Event: savings_lookahead_negative_balance** → If net savings is negative.

• **Event: savings_lookahead_positive_balance** → If net savings is positive.







# Earned in Current month

![[Pasted image 20250208093032.png]]


**1. Screen Name & Purpose**

• **Screen Name:** Earned in February

• **Purpose:** Displays a breakdown of the user’s **total income for the month**, categorized into **Regular Income**, **Hustles**, and **Gift Me!** contributions.

• **User Benefit:** Helps users understand **where their income is coming from** and encourages diversification through side hustles or GiftMe links.

**2. Key Features & Functionality**

  

**A. Displayed Information**

12. **Regular Income**

• **What It Shows:** Total income from stable sources, such as salaries, stipends, or recurring deposits.
ACTUAL Income.   
Minus internal / net-zero transactions.  

• **Description Text:** “Regular Salary and Income.”

• **Displayed Format:** "£X,XXX" (always positive, formatted in red).

13. **Hustles**

• **What It Shows:** Income earned through one-off activities like freelance gigs, side hustles, or ad hoc work.
- excluding Net-Zero Internal transactions. 
• **Description Text:** “A little (or a lot) more on the side.”

• **Displayed Format:** "£X,XXX" (always positive, defaults to £0 if no income logged).

14. **Gift Me!**

TODO Show contributions and also the entry point for creating Gift Links 
• **What It Shows:** Contributions from family or friends via **GiftMe links** shared through the app.

• **Description Text:** “Give your Fam a giftlink to your Saving Goals for your prezzies or just because.”

• **Displayed Format:** "£X,XXX" (always positive, defaults to £0 if no contributions received).

**3. Data Requirements & Calculation Logic**

  

**A. Data Fields Required**

|**Field**|**Description**|**Source**|
|---|---|---|
|regular_income[]|List of all regular income transactions for the month|Bank API (Saltedge)|
|hustle_income[]|List of all one-off hustle income transactions|Bank API (Saltedge)|
|gift_income[]|List of contributions via GiftMe links|Trustie GiftMe API|

**B. Calculation Logic**

15. **Regular Income**

• **Formula:** Sum of all transactions tagged as “regular income.”

• **Example Calculation:**

```
regular_income_total = sum(transaction["amount"] for transaction in regular_income)
```

  

• **Sample Data (API Response):**

```
{
  "transactions": [
    { "source": "Salary", "amount": 16000, "date": "2024-02-01" },
    { "source": "Rental Income", "amount": 874, "date": "2024-02-05" }
  ],
  "regular_income_total": 16874
}
```

  

16. **Hustles**

• **Formula:** Sum of all transactions tagged as “hustle income.”

• **Example Calculation:**

```
hustle_income_total = sum(transaction["amount"] for transaction in hustle_income)
```

  

• **Sample Data (API Response):**

```
{
  "transactions": [
    { "source": "Freelance Project", "amount": 300, "date": "2024-02-10" },
    { "source": "Odd Job", "amount": 200, "date": "2024-02-15" }
  ],
  "hustle_income_total": 500
}
```

  

17. **Gift Me!**

• **Formula:** Sum of all contributions received through GiftMe links.

• **Example Calculation:**

```
gift_income_total = sum(transaction["amount"] for transaction in gift_income)
```

  

• **Sample Data (API Response):**

```
{
  "transactions": [
    { "source": "Family Contribution", "amount": 50, "date": "2024-02-12" },
    { "source": "Friend Donation", "amount": 100, "date": "2024-02-20" }
  ],
  "gift_income_total": 150
}
```

**4. Error Handling & Edge Cases**

|**Scenario**|**Expected Behavior**|
|---|---|
|No regular income this month|Display £0 with placeholder text: “No regular income recorded yet.”|
|No hustle income this month|Display £0 with placeholder text: “No hustle income recorded yet.”|
|No GiftMe contributions|Display £0 with placeholder text: “No contributions received yet. Share your GiftMe link!”|
|API failure|Show error message: “Unable to fetch income details. Please try again.”|
|Currency mismatch (e.g., foreign income)|Convert all amounts to GBP using exchange rates.|

**5. UI/UX Behavior**

• **Loading State:** Show skeleton UI while fetching income data.

• **Animations:** Use smooth number transitions when data is updated.

• **Color Coding:**

• **Positive Income Values:** Always red.

• **£0 Values:** Display in a lighter shade to indicate inactivity.

• **Tooltips:** Add a “?” icon next to **Hustles** and **Gift Me!** to explain these income types.

**6. Success Criteria & Testing Guidelines**

  

✅ Regular, hustle, and GiftMe income totals are correctly calculated and displayed.

✅ API errors are handled gracefully with retry options.

✅ Displays “£0” for categories with no income logged.

✅ Currency is converted correctly for foreign transactions.

**7. Analytics & Tracking**

• **Event: regular_income_viewed** → When the Regular Income section is loaded.

• **Event: hustle_income_viewed** → When the Hustle section is loaded.

• **Event: giftme_link_shared** → When a user shares their GiftMe link.

• **Event: giftme_income_received** → When a contribution via GiftMe is received.

**Next Steps**

  

# Trustz in {current month}


![[Pasted image 20250208093317.png]]


# Spending Pockets

![[Pasted image 20250208093342.png]]


**1. Screen Name & Purpose**

• **Screen Name:** Spending Pockets

• **Purpose:** Digital equivalent of the **“envelope stuffing” budgeting method**, allowing users to allocate a fixed amount to different spending categories.

• **User Benefit:**

• Encourages **intentional spending** by pre-allocating money into predefined categories.

• Provides **real-time tracking** of spending against budgets.

• Helps users **avoid overspending** by deducting transactions automatically.

**2. Key Features & Functionality**

  

**A. Displayed Information**

  

Each **Spending Pocket** consists of:

• **Category Name** (e.g., Clothing, Groceries, Entertainment).

• **Budget Set (if applicable)** → Default is “No Budget” if the user hasn’t allocated an amount.

• **Current Spend** → Automatically updated as transactions are categorized.

  

**B. Core Functionalities**

1. **Creating & Allocating Money to Pockets**

• Users manually **set a budget** for each pocket (e.g., “£100 for Eating Out”).

• They can **edit, delete, or adjust allocations** at any time.

2. **Automatic Transaction Deduction**

• Transactions **pulled via Saltedge** are automatically deducted from the appropriate pocket based on **merchant/category mapping**.

• If a transaction doesn’t match a pocket, it stays **unclassified** until manually assigned.

1. **Budget Monitoring & Alerts**

• Users see a **progress bar or spending indicator** for each pocket.

• Alerts for:

• **Low balance warnings** (e.g., “Only £10 left in Groceries”).

• **Overbudget notifications** (e.g., “You’ve exceeded your Entertainment budget by £15”).

2. **See All Button**

• Expands to show a **detailed breakdown** of spending across all pockets.

**3. Data Requirements & Calculation Logic**

  

**A. Data Fields Required**

|**Field**|**Description**|**Source**|
|---|---|---|
|pocket_name|Name of the spending pocket|Trustie App|
|allocated_budget|Amount user assigned to the pocket|Trustie App (User Input)|
|spent_amount|Sum of all categorized transactions in the pocket|Computed Value|
|remaining_balance|allocated_budget - spent_amount|Computed Value|
|transactions[]|List of transactions assigned to each pocket|Bank API (Saltedge)|

**B. Calculation Logic**

3. **Remaining Balance Calculation**

• Example:

```
Allocated Budget: £200 (Eating Out)
Total Spent: £75
Remaining: £125
```

  

4. **Auto-Categorization via Merchant Matching**

• Each transaction is **matched to a Spending Pocket** based on:

• Merchant category (e.g., “Tesco” → Groceries).

• User-defined rules (e.g., recurring charges for Netflix → Entertainment).

• If no match is found, transaction remains **“Unassigned”** until manually categorized.

**4. Error Handling & Edge Cases**

|**Scenario**|**Expected Behavior**|
|---|---|
|No budget set for a pocket|Display “No Budget” instead of an allocated amount.|
|Transaction doesn’t match any pocket|Mark as “Unassigned” with prompt to categorize.|
|User overspends a pocket|Show red warning: “Over budget by £X.”|
|API failure fetching transactions|Show error: “Unable to sync spending data.”|
|User wants to edit a pocket|Allow **adjusting budget** even mid-month.|

**5. UI/UX Behavior**

• **Loading State:** Show placeholder “Loading your Spending Pockets…” while fetching data.

• **Visual Progress Bars:**

• **Green** = Plenty of budget left.

• **Orange** = Getting close to limit.

• **Red** = Overspent.

• **Tappable Pockets:** Clicking on a pocket shows **transaction details**.

• **Animations:** Smooth number updates as transactions sync.

**6. Success Criteria & Testing Guidelines**

  

✅ Users can **allocate budgets** and see their spending deducted automatically.

✅ Transactions are **correctly categorized** into spending pockets.

✅ Users receive **alerts** when approaching or exceeding budgets.

✅ Edge cases (e.g., missing transactions, manual re-categorization) work smoothly.

**7. Analytics & Tracking**

• **Event: spending_pockets_viewed** → When user opens Spending Pockets.

• **Event: budget_set** → When user sets or adjusts a budget.

• **Event: transaction_categorized** → When a transaction is added to a pocket.

• **Event: over_budget_alert_triggered** → When a pocket exceeds its limit.

**Next Steps**

✅  add  **forecasting features** (e.g., predicting spending trends)?




# Spending Pockets Details (drill down view)


![[Pasted image 20250208094458.png]]


**1. Screen Name & Purpose**

• **Screen Name:** Spending Pocket Detail

• **Purpose:** Provides a **detailed view of a specific Spending Pocket**, allowing users to set a budget, track spending, and review past transactions.

• **User Benefit:**

• Helps users **control spending** by setting a category-specific budget.

• Tracks **real-time spending deductions** from the allocated budget.

• Encourages **financial awareness** by answering: _Where did my money go?_

**2. Key Features & Functionality**

  

**A. Displayed Information**

1. **Pocket Overview**

• **Category Name & Icon** (e.g., Clothing 🛍️).

• **Budget Input Field** → User enters a spending limit.

• **Timeframe Selection** → Budget can be set:

• **Per Week**

• **Per Month** (Default)

• **One-Time Budget**

• **Recurring (From Now On)**

2. **Spending Summary**

• **Total Spent This Month** (Spend £X) → Sum of transactions categorized under this pocket.

• **Remaining Balance in Pocket** (Left in this pocket: £X) → Deducts real-time transactions from the budget.

1. **Where Did My Money Go? (Transaction Breakdown)**

• Lists **all transactions assigned to this pocket**.

• If no transactions exist, displays **“No transaction to be displayed 🤔”**.

• Allows users to **search transactions** related to this pocket.

2. **Close Pocket Button**

• Lets users **disable or delete the Spending Pocket**.

**3. Data Requirements & Calculation Logic**

  

**A. Data Fields Required**

|**Field**|**Description**|**Source**|
|---|---|---|
|pocket_name|Name of the spending pocket|Trustie App|
|budget_amount|User-defined spending limit|Trustie App (User Input)|
|spent_amount|Total sum of transactions under this pocket|Computed Value|
|remaining_balance|budget_amount - spent_amount|Computed Value|
|transactions[]|List of categorized transactions|Bank API (Saltedge)|

**B. Calculation Logic**

3. **Remaining Budget Calculation**

• Example:

```
Budget: £100 (Clothing)
Total Spent: £40
Remaining: £60
```

  

4. **Transaction Deduction**

• Transactions **pulled via Saltedge** are **automatically deducted** when categorized into this pocket.

• If a transaction is re-categorized, the spending is **adjusted accordingly**.

**4. Error Handling & Edge Cases**

|**Scenario**|**Expected Behavior**|
|---|---|
|No budget set for pocket|Display “No Budget” and allow manual input.|
|No transactions in pocket|Show placeholder: “No transaction to be displayed 🤔”|
|User overspends pocket|Show warning: “You have exceeded your budget by £X.”|
|API failure fetching transactions|Show error: “Unable to sync spending data.”|
|User wants to close pocket|Confirm action: “Are you sure you want to close this pocket?”|

**5. UI/UX Behavior**

• **Loading State:** Show placeholder “Loading pocket details…” while fetching data.

• **Animations:**

• Budget input smoothly updates remaining balance.

• Transactions animate in when categorized.

• **Color Coding:**

• **Red Warning** = Over Budget

• **Yellow Caution** = Near Limit

• **Green Safe** = Within Budget

• **Tappable Transactions:** Clicking a transaction **opens full details**.

**6. Success Criteria & Testing Guidelines**

  

✅ Users can **set or adjust a budget** for the spending pocket.

✅ Transactions are **correctly categorized** and deducted from the pocket.

✅ Users can **view past spending** and search for transactions.

✅ Edge cases (e.g., overspending, empty pockets) are handled smoothly.

**7. Analytics & Tracking**

• **Event: spending_pocket_opened** → When a user opens a pocket.

• **Event: budget_set** → When a user sets a budget.

• **Event: transaction_categorized** → When a transaction is added to a pocket.

• **Event: pocket_closed** → When a user disables a pocket.

**Next Steps**

✅ add  **AI-powered s (e.g., forecasted spending trends)?


# TODO Trend views for income and outgoings

- Trends for Income
- Trends for Spending Pockets
- 




# Mood Tags (Transaction Categorization Screen)

![[Pasted image 20250208094341.png]]

Shows only negative aka debit 
Include the Net-Zero. 
Show Positive Numbers.   

**1. Screen Name & Purpose**

• **Screen Name:** Mood Tags (Transaction Categorization)

• **Purpose:** Allows users to manually **assign a Money Mood, Spending Pocket, and Recurring status** to transactions for better tracking and financial awareness.

• **User Benefit:**

• Encourages **mindful spending reflection** through Money Moods.

• Helps users **organize transactions** into Spending Pockets for budgeting.

• Identifies **recurring transactions** to optimize expenses.

**2. Key Features & Functionality**

  

**A. Displayed Information**

1. **Transaction Details**

• **Date of transaction**

• **Merchant Name & Short Description** (truncated if long)

• **Transaction Amount** (formatted in red for debits)

• **Bank Account Used** (Masked Account Number)

2. **Categorization Options**

• **Money Mood** → User can select an emoji-based Money Mood category:

• 🤔 **Tag Me** (Uncategorized - needs review)

• 🏡 **Needs** (Essential expenses)

• 🎉 **Joy** (Experiences & happiness spending)

• 🛍️ **Wants** (Non-essential discretionary spending)

• 🐖 **Saving/Future You** (Investments & savings)

• **Spend Pocket** → Assigns transaction to a budget category (e.g., Clothing, Groceries).

• **Recurring Status** → User marks whether the transaction is **recurring or one-time**.

1. **Confirmation & Save Action**

• ✅ **Green Checkmark** → Confirms categorization is complete.

2. **See All Button**

• Expands to show a **full list of uncategorized transactions** for batch tagging.

**3. Data Requirements & Calculation Logic**

  

**A. Data Fields Required**

|**Field**|**Description**|**Source**|
|---|---|---|
|transaction_id|Unique transaction identifier|Bank API|
|transaction_date|Date of transaction|Bank API|
|merchant_name|Merchant or payee|Bank API|
|amount|Transaction value|Bank API|
|account_number_masked|Masked bank account number|Bank API|
|money_mood|User-assigned emotional spending tag|Trustie App (User Input)|
|spend_pocket|User-defined budgeting category|Trustie App (User Input)|
|recurring_status|Identifies if transaction is recurring|AI/Transaction Matching|

**B. Recurring Transaction Detection Logic**

3. **Pattern Recognition**

• Identifies transactions **with identical merchant names and similar amounts** recurring monthly.

• Flags transactions occurring **on the same date each month** (e.g., Rent, Subscriptions).

4. **Auto-Categorization Suggestions (Future Feature)**

• If a user categorizes a transaction, similar future transactions **will be auto-tagged** with the same settings.

**4. Error Handling & Edge Cases**

|**Scenario**|**Expected Behavior**|
|---|---|
|User does not categorize the transaction|Keeps “Tag Me” status and prompts later.|
|API failure fetching transaction data|Show error: “Unable to load transaction details.”|
|Duplicate transactions detected|Display warning: “Possible duplicate charge detected.”|
|User marks non-recurring transaction as recurring|Asks: “Are you sure? This transaction doesn’t repeat monthly.”|

**5. UI/UX Behavior**

• **Loading State:** Show a placeholder “Fetching transaction details…” while loading.

• **Animations:**

• Swipe gestures to **assign Money Mood quickly**.

• Tapping **recurring toggle** animates between ✅ and ❌.

• **Color Coding:**

• **Red:** Debits.

• **Green:** Credits.

• **Gray:** Uncategorized transactions needing action.

**6. Success Criteria & Testing Guidelines**

  

✅ Users can **assign a Money Mood, Spend Pocket, and Recurring status** to transactions.

✅ Transactions update **instantly** in reports after categorization.

✅ System correctly **detects recurring transactions**.

✅ Handles missing or duplicate transactions smoothly.

**7. Analytics & Tracking**

• **Event: transaction_categorized** → When a user assigns a Money Mood.

• **Event: spend_pocket_assigned** → When a transaction is added to a budgeting category.

• **Event: recurring_status_updated** → When a user marks a transaction as recurring.

• **Event: batch_tagging_completed** → When multiple transactions are categorized at once.

**Next Steps**


✅ Add **AI-powered auto-suggestions** for Money Moods based on past behavior?

  
# Recurring Spend

![[Pasted image 20250208094721.png]]

**1. Screen Name & Purpose**

• **Screen Name:** Recurring Spend

• **Purpose:** Helps users **identify, track, and manage recurring expenses**, such as subscriptions, memberships, and recurring bills.

• **User Benefit:**

• Encourages **awareness of recurring charges** to avoid unnecessary spending.

• Helps users **cancel unused subscriptions** to save money.

• Provides **smart insights** into long-term spending habits.

**2. Key Features & Functionality**

  

**A. Displayed Information**

5. **Recurring Spend Summary**

• **Section Title:** “Recurring Spend”

• **Informational Text:** Explains the importance of reviewing recurring payments and optimizing budgeting.

6. **Transaction List (Recurring Payments)**

• Displays a **list of identified recurring transactions** (e.g., Netflix, gym membership, insurance payments).

• **Each item includes:**

• **Date** of last charge

• **Merchant name & category** (e.g., Spotify – Entertainment)

• **Amount** (formatted as currency)

• If no recurring transactions are found, shows **“No transaction to be displayed 🤔”**.

7. **See All Button**

• Expands the list to show **all detected recurring payments**.

**3. Data Requirements & Calculation Logic**

  

**A. Data Fields Required**

|**Field**|**Description**|**Source**|
|---|---|---|
|transactions[]|List of all transactions|Bank API (Saltedge)|
|recurring_flag|Identifies whether a transaction is recurring|AI/Transaction Matching|
|merchant_name|Name of the business or service|Bank API|
|last_payment_date|Last time the recurring transaction was detected|Bank API|
|amount|Amount charged for the recurring transaction|Bank API|

**B. Recurring Transaction Detection Logic**

8. **Pattern Recognition**

• Identifies transactions that **repeat on a predictable cycle** (weekly, monthly, annually).

• Matches **merchant names** to known subscription-based services (e.g., Netflix, Amazon Prime).

9. **Calculation of Monthly Impact**

• **Formula:**

• Example:

```
Netflix: £12.99
Gym Membership: £30.00
Spotify: £9.99
Total: £52.98 per month
```

**4. Error Handling & Edge Cases**

|**Scenario**|**Expected Behavior**|
|---|---|
|No recurring transactions detected|Show placeholder: “No transaction to be displayed 🤔”|
|User cancels a recurring subscription|Remove from the recurring list after one billing cycle confirms cancellation.|
|API failure fetching transactions|Show error: “Unable to sync recurring spend data.”|
|One-time charges mistakenly flagged|Allow manual removal or marking as “one-time.”|

**5. UI/UX Behavior**

• **Loading State:** Show placeholder “Scanning for recurring payments…” while fetching data.

• **Animations:**

• Transactions **slide in** when identified.

• Subscriptions **fade out** if canceled.

• **Color Coding:**

• **Red** = High-cost recurring subscriptions.

• **Yellow** = Mid-tier costs.

• **Green** = Small or infrequent charges.

**6. Success Criteria & Testing Guidelines**

  

✅ **Recurring transactions are correctly detected** using pattern analysis.

✅ Users can **review, confirm, or remove flagged transactions**.

✅ Users can **see total recurring spend per month**.

✅ Users receive **insights on potential savings** (e.g., highlighting unused subscriptions).

**7. Analytics & Tracking**

• **Event: recurring_spend_viewed** → When a user opens the screen.

• **Event: recurring_transaction_confirmed** → When a user marks a charge as recurring.

• **Event: recurring_transaction_removed** → When a user cancels a subscription.

• **Event: subscription_savings_suggested** → When the app suggests canceling an unused subscription.

**Next Steps**

✅ add a **“Cancel Subscription”** integration or **subscription reminders**?

  

# Flexible Money Left

![[Pasted image 20250208094814.png]]


**1. Screen Name & Purpose**

• **Screen Name:** Flexible Money Left (Look-Ahead)

• **Purpose:** Provides a **forecast of expected cash flow** for the month by summarizing **expected income, planned expenses, and available discretionary funds**.

• **User Benefit:**

• Helps users **anticipate their financial position** before the month ends.

• Encourages **smarter spending decisions** based on available money.

• Prevents overspending by **factoring in upcoming recurring expenses**.

**2. Key Features & Functionality**


**A. Displayed Information**

10. **Money In (Income Sources)**

• **Regular Income:** Expected salary, recurring deposits.

• **Side Hustles:** Additional earnings from freelance work, gig economy, or passive income.

11. **Money Out (Expenses & Savings)**

• **Auto Savings, Investments:** Money automatically moved into savings accounts or investment platforms.

• **Spent So Far:** Total expenses incurred so far this month.

12. **Out Coming Up (Future Expenses)**

• **Recurring Spend Coming Up:** Bills, subscriptions, or pre-planned expenses that will occur later in the month.

13. **Final Summary: Flexible Money Left**

• Shows the **remaining money available** after accounting for all **income, expenses, and upcoming costs**.

• Displays **current date and remaining days in the month** for better planning.

**3. Data Requirements & Calculation Logic**

  

**A. Data Fields Required**

|**Field**|**Description**|**Source**|
|---|---|---|
|regular_income|Expected salary and stable income|Bank API (Saltedge)|
|side_hustles_income|Earnings from freelance work or passive income|Bank API / Manual Input|
|auto_savings|Scheduled savings transfers & investments|Bank API|
|spent_so_far|Total amount spent so far this month|Computed Value|
|recurring_spend_upcoming|Bills & subscriptions expected later in the month|Recurring Spend Tracker|
|flexible_money_left|Available cash after accounting for income & expenses|Computed Value|

**B. Calculation Logic**

14. **Total Income Calculation**

15. **Total Expenses Calculation**

16. **Flexible Money Left Calculation**

  

• **Example Calculation:**

```
Regular Income: £2,500  
Side Hustles: £300  
Auto Savings & Investments: £400  
Spent So Far: £1,200  
Recurring Expenses Coming Up: £600  

Flexible Money Left = (2500 + 300) - (400 + 1200 + 600)  
                    = 2800 - 2200  
                    = £600 available
```

**4. Error Handling & Edge Cases**

|**Scenario**|**Expected Behavior**|
|---|---|
|No recorded income|Display “No income recorded yet” with a prompt to update.|
|No side hustle income|Show “No additional earnings recorded.”|
|No expenses recorded yet|Display “No spending yet—track as you go!”|
|Recurring expenses exceed income|Show warning: “You may run out of funds before month-end.”|
|API failure fetching transactions|Show error: “Unable to fetch income/expense data.”|

**5. UI/UX Behavior**

• **Loading State:** Show a skeleton UI while fetching data.

• **Animated Progress Bars:** Display money-in vs. money-out visually.

• **Color Coding:**

• **Green:** Positive cash flow.

• **Yellow:** Neutral (breaking even).

• **Red:** Negative cash flow (risk of overspending).

• **Expandable Sections:** Users can collapse/expand **Money In & Money Out** sections.

**6. Success Criteria & Testing Guidelines**

  

✅ Income, expenses, and savings are correctly displayed.

✅ Users can track **remaining flexible money** dynamically.

✅ System handles edge cases (e.g., missing data, unexpected expenses).

✅ UI remains clear and responsive on all device sizes.

**7. Analytics & Tracking**

• **Event: flexible_money_viewed** → When a user opens the screen.

• **Event: income_updated** → When a user manually adjusts expected income.

• **Event: expense_recorded** → When a new expense is detected.

• **Event: low_balance_warning** → Triggered when upcoming expenses exceed available funds.

**Next Steps**

✅ Add a **“Smart Spending Suggestion”** feature (e.g., AI-based saving tips)?

  



# Where did my Money go

![[Pasted image 20250208094947.png]]



**1. Screen Name & Purpose**

• **Screen Name:** Where Did My Money Go? (Latest Transactions)

• **Purpose:** Provides a **detailed view of recent spending activity**, helping users track where their money is going.

• **User Benefit:**

• Offers **full transparency** on past transactions.

• Encourages **spending reflection** to promote mindful financial habits.

• Allows users to **categorize transactions** for better budgeting.

**2. Key Features & Functionality**

  

**A. Displayed Information**

17. **Total Spent This Month (Spending Overview)**

• Displays **total spending for the current month**.

• Progress bar shows spending progress **against a monthly budget (if set)**.

• If no transactions exist, displays **“No transaction to display 🤔”**.

18. **Latest Transactions List**

• **Each transaction includes:**

• **Date** of transaction.

• **Merchant Name & Category** (e.g., “Land & Property SE – Monthly”).

• **Transaction Amount** (formatted in red for debits).

• **Money Mood Icon** (if categorized by user).

• If a transaction is unclassified, it is marked with **🤔 (Tag Me)** to prompt user categorization.

19. **See All Button**

• Expands to show **full transaction history**.

**3. Data Requirements & Calculation Logic**

  

**A. Data Fields Required**

|**Field**|**Description**|**Source**|
|---|---|---|
|transactions[]|List of all recent transactions|Bank API (Saltedge)|
|transaction_date|Date of transaction|Bank API|
|merchant_name|Merchant where transaction occurred|Bank API|
|amount|Transaction value (negative for debits)|Bank API|
|category|User-assigned spending category (e.g., Rent, Groceries)|Trustie App (User Input)|
|money_mood|Emotion tag assigned by user|Trustie App (User Input)|

**B. Spending Calculation Logic**

20. **Total Spending for the Month**

21. **Categorization Logic**

• Transactions **auto-categorized** based on:

• **Merchant name** (e.g., Netflix → Entertainment).

• **Recurring pattern detection** (e.g., Rent payments marked as “Monthly”).

• **User input** (manual tagging).

**4. Error Handling & Edge Cases**

|**Scenario**|**Expected Behavior**|
|---|---|
|No transactions recorded|Show placeholder: “No transaction to display 🤔”|
|API failure fetching transactions|Show error: “Unable to fetch spending data.”|
|Unclassified transactions|Display **🤔 (Tag Me)** icon to prompt user action.|
|Duplicate transactions detected|Flag for review with a warning.|

**5. UI/UX Behavior**

• **Loading State:** Show a placeholder “Fetching latest transactions…” while data loads.

• **Color Coding:**

• **Red:** Money spent (debits).

• **Green:** Money received (credits).

• **🤔 (Tag Me):** Unclassified transactions needing user review.

• **Expandable Sections:**

• Users can **tap transactions** to view details or categorize.

**6. Success Criteria & Testing Guidelines**

  

✅ Transactions are **correctly displayed and categorized**.

✅ **Total spending for the month updates dynamically**.

✅ Users can **manually classify transactions** with Money Moods.

✅ Edge cases (e.g., missing transactions, API failures) are handled properly.

**7. Analytics & Tracking**

• **Event: transactions_viewed** → When a user opens the transactions list.

• **Event: transaction_categorized** → When a user assigns a Money Mood to a transaction.

• **Event: transaction_flagged_duplicate** → When the system detects a potential duplicate charge.

**Next Steps**

✅ Add **AI-powered categorization suggestions**?

  


# Latest Transactions


Shows ALL TRANSACTIONS 


![[Pasted image 20250208095114.png]]


**1. Screen Name & Purpose**

• **Screen Name:** Where Did My Money Go? (Latest Transactions)

• **Purpose:** Provides a **detailed view of recent spending activity**, helping users track where their money is going.

• **User Benefit:**

• Offers **full transparency** on past transactions.

• Encourages **spending reflection** to promote mindful financial habits.

• Allows users to **categorize transactions** for better budgeting.

**2. Key Features & Functionality**

  

**A. Displayed Information**

22. **Total Spent This Month (Spending Overview)**

• Displays **total spending for the current month**.

• Progress bar shows spending progress **against a monthly budget (if set)**.

• If no transactions exist, displays **“No transaction to display 🤔”**.

23. **Latest Transactions List**

• **Each transaction includes:**

• **Date** of transaction.

• **Merchant Name & Category** (e.g., “Land & Property SE – Monthly”).

• **Transaction Amount** (formatted in red for debits).

• **Money Mood Icon** (if categorized by user).

• If a transaction is unclassified, it is marked with **🤔 (Tag Me)** to prompt user categorization.

24. **See All Button**

• Expands to show **full transaction history**.

**3. Data Requirements & Calculation Logic**

  

**A. Data Fields Required**

|**Field**|**Description**|**Source**|
|---|---|---|
|transactions[]|List of all recent transactions|Bank API (Saltedge)|
|transaction_date|Date of transaction|Bank API|
|merchant_name|Merchant where transaction occurred|Bank API|
|amount|Transaction value (negative for debits)|Bank API|
|category|User-assigned spending category (e.g., Rent, Groceries)|Trustie App (User Input)|
|money_mood|Emotion tag assigned by user|Trustie App (User Input)|

**B. Spending Calculation Logic**

25. **Total Spending for the Month**

26. **Categorization Logic**

• Transactions **auto-categorized** based on:

• **Merchant name** (e.g., Netflix → Entertainment).

• **Recurring pattern detection** (e.g., Rent payments marked as “Monthly”).

• **User input** (manual tagging).

**4. Error Handling & Edge Cases**

|**Scenario**|**Expected Behavior**|
|---|---|
|No transactions recorded|Show placeholder: “No transaction to display 🤔”|
|API failure fetching transactions|Show error: “Unable to fetch spending data.”|
|Unclassified transactions|Display **🤔 (Tag Me)** icon to prompt user action.|
|Duplicate transactions detected|Flag for review with a warning.|

**5. UI/UX Behavior**

• **Loading State:** Show a placeholder “Fetching latest transactions…” while data loads.

• **Color Coding:**

• **Red:** Money spent (debits).

• **Green:** Money received (credits).

• **🤔 (Tag Me):** Unclassified transactions needing user review.

• **Expandable Sections:**

• Users can **tap transactions** to view details or categorize.

**6. Success Criteria & Testing Guidelines**

  

✅ Transactions are **correctly displayed and categorized**.

✅ **Total spending for the month updates dynamically**.

✅ Users can **manually classify transactions** with Money Moods.

✅ Edge cases (e.g., missing transactions, API failures) are handled properly.

**7. Analytics & Tracking**

• **Event: transactions_viewed** → When a user opens the transactions list.

• **Event: transaction_categorized** → When a user assigns a Money Mood to a transaction.

• **Event: transaction_flagged_duplicate** → When the system detects a potential duplicate charge.

**Next Steps**

✅ add **AI-powered categorization suggestions**?

  



















