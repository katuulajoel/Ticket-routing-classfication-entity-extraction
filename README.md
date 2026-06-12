# Customer Support Automation Challenge

## Overview

Build a customer support automation system using classic language modeling techniques. Your goal is to implement text classification for ticket routing and rule-based entity extraction for customer details, automating manual copy-paste workflows.

## Problem Statement

Customer support agents currently copy and paste email text into multiple systems: one for routing tickets to specialist queues and another for logging customer details. Your task is to deliver a proof-of-concept that automates both workflows using the same ticket data.

**Required Components:**
- Text classification to automatically route tickets based on historical examples
- Entity extraction to surface customer details directly to the agent dashboard

## Files to Implement

- `src/data_loader.py`: Load and validate ticket CSV data
- `src/ticket_router.py`: sklearn-based text classification pipeline with confidence scoring
- `src/entity_extractor.py`: Rule-based entity extraction using regex patterns

## Success Criteria

Your implementation will be evaluated on these criteria:
- **Data loading**: Correctly reads CSV, validates columns, handles errors gracefully
- **Classification accuracy**: Naive Bayes model achieves acceptable routing performance
- **Confidence scoring**: Low-confidence predictions routed to manual review queue
- **Entity extraction**: Accurate detection of names, emails, phones, monetary amounts
- **Code quality**: Clean, efficient, well-documented implementation

## Time Limit

30 minutes

## Dataset

The challenge uses customer support ticket data located in `data/support_tickets.csv`.

**Dataset Features:**
- `ticket_id`: Unique ticket identifier
- `customer_email`: Customer contact email
- `subject`: Ticket subject line
- `message`: Full ticket message text
- `category`: Target routing category (billing, technical, sales, general)

## Implementation Details

### Task 1: `src/data_loader.py`

**Requirements:**
- Implement `load_ticket_data` function
- Read CSV file and validate required columns
- Return clean ticket records for downstream processing
- Provide helpful error messages for missing files or invalid data
---

### Task 2: `src/ticket_router.py`

**Requirements:**
- Implement `TicketRouter` class using sklearn
- Vectorize text with TfidfVectorizer or CountVectorizer
- Train Naive Bayes classifier on historical ticket data
- Expose `predict_with_confidence` method
- Route low-confidence predictions to manual review queue
---

### Task 3: `src/entity_extractor.py`

**Requirements:**
- Implement `EntityExtractor` class with regex-based extraction
- Detect person names, email addresses, phone numbers, monetary amounts
- Provide both extraction and inline annotation utilities
- Use efficient regex patterns for production readiness
---

# Ticket-routing-classfication-entity-extraction
