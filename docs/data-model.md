# Data Model

## Overview

The Di Cho Tien Loi platform uses a normalized relational database schema designed for multi-tenant food management. The database is built on PostgreSQL 15 and uses SQLAlchemy ORM with Alembic for migrations.

## Entity Relationship Diagram

```
┌─────────────┐    ┌─────────────────┐    ┌─────────────┐
│    users    │    │ group_members   │    │   groups    │
├─────────────┤    ├─────────────────┤    ├─────────────┤
│ id (PK)     │◄─┐ │ id (PK)         │ ┌─►│ id (PK)     │
│ email       │  └─│ user_id (FK)    │ │  │ name        │
│ password_h  │    │ group_id (FK)   │─┘  │ description │
│ name        │    │ role            │    │ owner_id(FK)│
│ username    │    │ joined_at       │    │ created_at  │
│ avatar_url  │    │ is_active       │    └─────────────┘
│ language    │    └─────────────────┘
│ timezone    │
│ is_active   │
│ is_verified │
│ created_at  │
│ updated_at  │
└─────────────┘

┌─────────────┐    ┌─────────────┐
│ categories  │    │    units    │
├─────────────┤    ├─────────────┤
│ id (PK)     │    │ id (PK)     │
│ name        │    │ name        │
│ description │    │ symbol      │
│ color       │    │ type        │
│ icon        │    │ group_id(FK)│
│ group_id(FK)│    │ created_at  │
│ created_by  │    └─────────────┘
│ created_at  │
└─────────────┘

                   ┌─────────────┐
                   │    foods    │
                   ├─────────────┤
┌─────────────┐    │ id (PK)     │    ┌─────────────┐
│ categories  │◄───│ category_id │    │    units    │
└─────────────┘    │ unit_id     │───►└─────────────┘
                   │ name        │
                   │ description │
                   │ image_url   │
                   │ barcode     │
                   │ brand       │
                   │ nutritional │
                   │ group_id(FK)│
                   │ created_by  │
                   │ created_at  │
                   │ updated_at  │
                   └─────────────┘
                          │
                          │
              ┌───────────┴─────────────┐
              │                         │
              ▼                         ▼
    ┌─────────────────┐      ┌──────────────────┐
    │  fridge_items   │      │ shopping_tasks   │
    ├─────────────────┤      ├──────────────────┤
    │ id (PK)         │      │ id (PK)          │
    │ food_id (FK)    │      │ list_id (FK)     │
    │ group_id (FK)   │      │ food_id (FK)     │
    │ quantity        │      │ quantity         │
    │ note            │      │ note             │
    │ purchase_date   │      │ is_done          │
    │ use_within_date │      │ done_at          │
    │ location        │      │ done_by          │
    │ is_opened       │      │ priority         │
    │ opened_at       │      │ created_at       │
    │ created_by      │      │ updated_at       │
    │ created_at      │      └──────────────────┘
    │ updated_at      │                │
    └─────────────────┘                │
                                       ▲
                              ┌─────────────────┐
                              │ shopping_lists  │
                              ├─────────────────┤
                              │ id (PK)         │
                              │ name            │
                              │ description     │
                              │ group_id (FK)   │
                              │ assign_to (FK)  │
                              │ due_date        │
                              │ priority        │
                              │ status          │
                              │ is_archived     │
                              │ created_by      │
                              │ created_at      │
                              │ updated_at      │
                              └─────────────────┘

┌─────────────────┐      ┌──────────────────────┐
│   meal_plans    │      │   meal_plan_items    │
├─────────────────┤      ├──────────────────────┤
│ id (PK)         │◄─────│ id (PK)              │
│ name            │      │ meal_plan_id (FK)    │
│ description     │      │ food_id (FK)         │
│ group_id (FK)   │      │ quantity             │
│ plan_date       │      │ notes                │
│ meal_type       │      │ sequence_order       │
│ servings        │      │ created_at           │
│ recipe_id (FK)  │      └──────────────────────┘
│ status          │
│ notes           │
│ created_by      │
│ created_at      │
│ updated_at      │
└─────────────────┘

┌─────────────┐      ┌─────────────────┐
│   recipes   │      │ recipe_steps    │
├─────────────┤      ├─────────────────┤
│ id (PK)     │◄─────│ id (PK)         │
│ name        │      │ recipe_id (FK)  │
│ description │      │ step_number     │
│ instructions│      │ instruction     │
│ prep_time   │      │ duration        │
│ cook_time   │      │ temperature     │
│ servings    │      │ notes           │
│ difficulty  │      │ image_url       │
│ cuisine_type│      │ created_at      │
│ image_url   │      └─────────────────┘
│ nutrition   │
│ tags        │
│ group_id(FK)│
│ food_id(FK) │
│ created_by  │
│ created_at  │
│ updated_at  │
└─────────────┘

┌─────────────┐
│ audit_logs  │
├─────────────┤
│ id (PK)     │
│ user_id(FK) │
│ group_id(FK)│
│ entity_type │
│ entity_id   │
│ action      │
│ old_values  │
│ new_values  │
│ ip_address  │
│ user_agent  │
│ created_at  │
└─────────────┘
```

## Core Tables

### users
Stores user account information and authentication data.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique user identifier
- `email` (VARCHAR(255) UNIQUE NOT NULL): User's email address, used for login
- `password_hash` (VARCHAR(255) NOT NULL): Bcrypt hashed password
- `name` (VARCHAR(100) NOT NULL): User's display name
- `username` (VARCHAR(50) UNIQUE): Optional unique username
- `avatar_url` (TEXT): URL to user's profile picture
- `language` (VARCHAR(5) DEFAULT 'en'): Preferred language code (ISO 639-1)
- `timezone` (VARCHAR(50) DEFAULT 'UTC'): User's timezone identifier
- `is_active` (BOOLEAN DEFAULT true): Whether account is active
- `is_verified` (BOOLEAN DEFAULT false): Whether email is verified
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())
- `updated_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `email`
- UNIQUE INDEX on `username`
- INDEX on `is_active, is_verified`

### groups
Represents household or family units that share food management.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique group identifier
- `name` (VARCHAR(100) NOT NULL): Group display name
- `description` (TEXT): Optional group description
- `owner_id` (INTEGER NOT NULL REFERENCES users(id)): Group owner
- `settings` (JSONB): Group-specific settings
- `invite_code` (VARCHAR(20) UNIQUE): Invitation code for joining
- `is_active` (BOOLEAN DEFAULT true): Whether group is active
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())
- `updated_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY on `owner_id` REFERENCES `users(id)`
- UNIQUE INDEX on `invite_code`
- INDEX on `is_active`

### group_members
Join table managing user membership in groups with roles.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique membership identifier
- `user_id` (INTEGER NOT NULL REFERENCES users(id)): Member user
- `group_id` (INTEGER NOT NULL REFERENCES groups(id)): Target group
- `role` (VARCHAR(20) NOT NULL CHECK role IN ('owner', 'admin', 'member')): Member role
- `permissions` (JSONB): Role-specific permissions
- `is_active` (BOOLEAN DEFAULT true): Whether membership is active
- `joined_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())
- `left_at` (TIMESTAMP WITH TIME ZONE): When user left the group

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY on `user_id` REFERENCES `users(id)`
- FOREIGN KEY on `group_id` REFERENCES `groups(id)`
- UNIQUE INDEX on `user_id, group_id`
- INDEX on `group_id, is_active`

### categories
Food categories for organization and filtering.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique category identifier
- `name` (VARCHAR(50) NOT NULL): Category name
- `description` (TEXT): Category description
- `color` (VARCHAR(7)): Hex color code for UI display
- `icon` (VARCHAR(50)): Icon identifier for UI
- `group_id` (INTEGER REFERENCES groups(id)): Group scope (NULL for system categories)
- `parent_id` (INTEGER REFERENCES categories(id)): Parent category for hierarchy
- `sort_order` (INTEGER DEFAULT 0): Display order
- `is_active` (BOOLEAN DEFAULT true): Whether category is active
- `created_by` (INTEGER REFERENCES users(id)): Creator user
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY on `group_id` REFERENCES `groups(id)`
- FOREIGN KEY on `parent_id` REFERENCES `categories(id)`
- FOREIGN KEY on `created_by` REFERENCES `users(id)`
- INDEX on `group_id, is_active`
- INDEX on `parent_id`

### units
Measurement units for quantities.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique unit identifier
- `name` (VARCHAR(20) NOT NULL): Unit name (e.g., "kg", "lbs", "pieces")
- `symbol` (VARCHAR(10)): Unit symbol or abbreviation
- `type` (VARCHAR(20) NOT NULL CHECK type IN ('weight', 'volume', 'count', 'length')): Unit type
- `base_unit_id` (INTEGER REFERENCES units(id)): Base unit for conversions
- `conversion_factor` (DECIMAL(10,6)): Factor to convert to base unit
- `group_id` (INTEGER REFERENCES groups(id)): Group scope (NULL for system units)
- `is_active` (BOOLEAN DEFAULT true): Whether unit is active
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY on `base_unit_id` REFERENCES `units(id)`
- FOREIGN KEY on `group_id` REFERENCES `groups(id)`
- INDEX on `group_id, is_active`
- INDEX on `type`

### foods
Food item definitions within groups.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique food identifier
- `name` (VARCHAR(100) NOT NULL): Food name
- `description` (TEXT): Food description
- `category_id` (INTEGER REFERENCES categories(id)): Food category
- `unit_id` (INTEGER NOT NULL REFERENCES units(id)): Default unit
- `image_url` (TEXT): URL to food image
- `barcode` (VARCHAR(50)): Product barcode
- `brand` (VARCHAR(50)): Brand name
- `nutritional_info` (JSONB): Nutritional information
- `default_shelf_life_days` (INTEGER): Default shelf life in days
- `storage_instructions` (TEXT): Storage recommendations
- `group_id` (INTEGER NOT NULL REFERENCES groups(id)): Owner group
- `is_active` (BOOLEAN DEFAULT true): Whether food is active
- `created_by` (INTEGER NOT NULL REFERENCES users(id)): Creator user
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())
- `updated_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY on `category_id` REFERENCES `categories(id)`
- FOREIGN KEY on `unit_id` REFERENCES `units(id)`
- FOREIGN KEY on `group_id` REFERENCES `groups(id)`
- FOREIGN KEY on `created_by` REFERENCES `users(id)`
- INDEX on `group_id, is_active`
- INDEX on `category_id`
- UNIQUE INDEX on `barcode, group_id`
- FULL TEXT INDEX on `name, description, brand`

### fridge_items
Current inventory items in the fridge/pantry.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique item identifier
- `food_id` (INTEGER NOT NULL REFERENCES foods(id)): Food reference
- `group_id` (INTEGER NOT NULL REFERENCES groups(id)): Owner group
- `quantity` (DECIMAL(8,3) NOT NULL): Quantity available
- `unit_id` (INTEGER REFERENCES units(id)): Quantity unit (overrides food default)
- `note` (TEXT): Additional notes
- `purchase_date` (DATE): When item was purchased
- `use_within_date` (DATE NOT NULL): Expiration or use-by date
- `location` (VARCHAR(50)): Storage location (fridge, pantry, freezer)
- `is_opened` (BOOLEAN DEFAULT false): Whether package is opened
- `opened_at` (TIMESTAMP WITH TIME ZONE): When item was opened
- `cost` (DECIMAL(8,2)): Purchase cost
- `created_by` (INTEGER NOT NULL REFERENCES users(id)): Creator user
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())
- `updated_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY on `food_id` REFERENCES `foods(id)`
- FOREIGN KEY on `group_id` REFERENCES `groups(id)`
- FOREIGN KEY on `unit_id` REFERENCES `units(id)`
- FOREIGN KEY on `created_by` REFERENCES `users(id)`
- INDEX on `group_id, use_within_date`
- INDEX on `use_within_date` (for expiry checks)
- INDEX on `food_id`

### shopping_lists
Shopping lists for groups.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique list identifier
- `name` (VARCHAR(100) NOT NULL): List name
- `description` (TEXT): List description
- `group_id` (INTEGER NOT NULL REFERENCES groups(id)): Owner group
- `assign_to_user_id` (INTEGER REFERENCES users(id)): Assigned shopper
- `due_date` (DATE): Target shopping date
- `priority` (VARCHAR(10) DEFAULT 'medium' CHECK priority IN ('low', 'medium', 'high')): List priority
- `status` (VARCHAR(20) DEFAULT 'active' CHECK status IN ('draft', 'active', 'completed', 'cancelled')): List status
- `budget` (DECIMAL(10,2)): Budget limit
- `total_cost` (DECIMAL(10,2) DEFAULT 0): Actual total cost
- `is_archived` (BOOLEAN DEFAULT false): Whether list is archived
- `created_by` (INTEGER NOT NULL REFERENCES users(id)): Creator user
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())
- `updated_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY on `group_id` REFERENCES `groups(id)`
- FOREIGN KEY on `assign_to_user_id` REFERENCES `users(id)`
- FOREIGN KEY on `created_by` REFERENCES `users(id)`
- INDEX on `group_id, is_archived`
- INDEX on `assign_to_user_id, status`
- INDEX on `due_date`

### shopping_tasks
Individual items within shopping lists.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique task identifier
- `list_id` (INTEGER NOT NULL REFERENCES shopping_lists(id) ON DELETE CASCADE): Parent list
- `food_id` (INTEGER NOT NULL REFERENCES foods(id)): Food to buy
- `quantity` (DECIMAL(8,3) NOT NULL): Quantity needed
- `unit_id` (INTEGER REFERENCES units(id)): Quantity unit
- `note` (TEXT): Task-specific notes
- `estimated_cost` (DECIMAL(8,2)): Estimated cost
- `actual_cost` (DECIMAL(8,2)): Actual cost when purchased
- `priority` (VARCHAR(10) DEFAULT 'medium' CHECK priority IN ('low', 'medium', 'high')): Task priority
- `is_done` (BOOLEAN DEFAULT false): Whether task is completed
- `done_at` (TIMESTAMP WITH TIME ZONE): When task was completed
- `done_by` (INTEGER REFERENCES users(id)): User who completed task
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())
- `updated_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY on `list_id` REFERENCES `shopping_lists(id)` ON DELETE CASCADE
- FOREIGN KEY on `food_id` REFERENCES `foods(id)`
- FOREIGN KEY on `unit_id` REFERENCES `units(id)`
- FOREIGN KEY on `done_by` REFERENCES `users(id)`
- INDEX on `list_id, is_done`
- INDEX on `food_id`

## Extended Tables (Future Features)

### meal_plans
Planned meals for specific dates and meal types.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique meal plan identifier
- `name` (VARCHAR(100) NOT NULL): Meal name
- `description` (TEXT): Meal description
- `group_id` (INTEGER NOT NULL REFERENCES groups(id)): Owner group
- `plan_date` (DATE NOT NULL): Planned date
- `meal_type` (VARCHAR(20) NOT NULL CHECK meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')): Meal type
- `servings` (INTEGER DEFAULT 1): Number of servings
- `recipe_id` (INTEGER REFERENCES recipes(id)): Associated recipe
- `status` (VARCHAR(20) DEFAULT 'planned' CHECK status IN ('planned', 'prepared', 'cancelled')): Meal status
- `notes` (TEXT): Planning notes
- `created_by` (INTEGER NOT NULL REFERENCES users(id)): Creator user
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())
- `updated_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

### meal_plan_items
Foods included in meal plans.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique item identifier
- `meal_plan_id` (INTEGER NOT NULL REFERENCES meal_plans(id) ON DELETE CASCADE): Parent meal plan
- `food_id` (INTEGER NOT NULL REFERENCES foods(id)): Required food
- `quantity` (DECIMAL(8,3) NOT NULL): Quantity needed
- `unit_id` (INTEGER REFERENCES units(id)): Quantity unit
- `notes` (TEXT): Item-specific notes
- `sequence_order` (INTEGER DEFAULT 0): Order in recipe
- `is_optional` (BOOLEAN DEFAULT false): Whether ingredient is optional
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

### recipes
Cooking recipes associated with foods.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique recipe identifier
- `name` (VARCHAR(100) NOT NULL): Recipe name
- `description` (TEXT): Recipe description
- `instructions` (TEXT NOT NULL): Cooking instructions
- `prep_time_minutes` (INTEGER): Preparation time
- `cook_time_minutes` (INTEGER): Cooking time
- `servings` (INTEGER DEFAULT 1): Number of servings
- `difficulty` (VARCHAR(10) CHECK difficulty IN ('easy', 'medium', 'hard')): Recipe difficulty
- `cuisine_type` (VARCHAR(50)): Cuisine classification
- `image_url` (TEXT): Recipe image URL
- `nutritional_info` (JSONB): Nutritional information per serving
- `tags` (TEXT[]): Recipe tags for searching
- `rating_avg` (DECIMAL(3,2)): Average user rating
- `rating_count` (INTEGER DEFAULT 0): Number of ratings
- `group_id` (INTEGER NOT NULL REFERENCES groups(id)): Owner group
- `food_id` (INTEGER REFERENCES foods(id)): Primary food this recipe is for
- `source_url` (TEXT): Original recipe URL
- `is_public` (BOOLEAN DEFAULT false): Whether recipe is shared publicly
- `created_by` (INTEGER NOT NULL REFERENCES users(id)): Creator user
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())
- `updated_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

### recipe_steps
Detailed cooking steps for recipes.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique step identifier
- `recipe_id` (INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE): Parent recipe
- `step_number` (INTEGER NOT NULL): Step sequence number
- `instruction` (TEXT NOT NULL): Step instruction
- `duration_minutes` (INTEGER): Time for this step
- `temperature` (INTEGER): Cooking temperature if applicable
- `notes` (TEXT): Additional step notes
- `image_url` (TEXT): Step illustration image
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

### audit_logs
System audit trail for tracking user actions.

**Fields:**
- `id` (SERIAL PRIMARY KEY): Unique log identifier
- `user_id` (INTEGER REFERENCES users(id)): User who performed action
- `group_id` (INTEGER REFERENCES groups(id)): Group context if applicable
- `entity_type` (VARCHAR(50) NOT NULL): Type of entity affected (users, foods, etc.)
- `entity_id` (INTEGER NOT NULL): ID of affected entity
- `action` (VARCHAR(20) NOT NULL): Action performed (create, update, delete, etc.)
- `old_values` (JSONB): Previous values before change
- `new_values` (JSONB): New values after change
- `metadata` (JSONB): Additional context data
- `ip_address` (INET): User's IP address
- `user_agent` (TEXT): User's browser/app information
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT NOW())

**Indexes:**
- PRIMARY KEY on `id`
- FOREIGN KEY on `user_id` REFERENCES `users(id)`
- FOREIGN KEY on `group_id` REFERENCES `groups(id)`
- INDEX on `user_id, created_at`
- INDEX on `entity_type, entity_id`
- INDEX on `created_at` (for archiving old logs)

## Data Relationships

### One-to-Many Relationships
- `users` → `group_members` (user can belong to multiple groups)
- `groups` → `group_members` (group can have multiple members)
- `groups` → `foods` (group can have multiple foods)
- `foods` → `fridge_items` (food can have multiple inventory entries)
- `shopping_lists` → `shopping_tasks` (list can have multiple tasks)
- `meal_plans` → `meal_plan_items` (meal can include multiple foods)
- `recipes` → `recipe_steps` (recipe can have multiple steps)

### Many-to-Many Relationships
- `users` ↔ `groups` (through `group_members`)
- `meal_plans` ↔ `foods` (through `meal_plan_items`)

### Optional Relationships
- `foods.category_id` → `categories.id` (food may not have category)
- `shopping_lists.assign_to_user_id` → `users.id` (list may not be assigned)
- `recipes.food_id` → `foods.id` (recipe may not be linked to specific food)

## Data Constraints and Rules

### Business Rules
1. **Group Ownership**: Every group must have exactly one owner
2. **User Uniqueness**: Email addresses must be unique across the system
3. **Group Membership**: Users cannot be members of the same group multiple times
4. **Expiry Dates**: `use_within_date` in fridge_items cannot be in the past when created
5. **Positive Quantities**: All quantity fields must be positive numbers
6. **Role Hierarchy**: Group owners automatically have admin permissions

### Data Validation
1. **Email Format**: Valid email format required for user registration
2. **Password Strength**: Minimum 8 characters with mixed case and numbers
3. **Date Formats**: All dates stored in ISO 8601 format with timezone
4. **Decimal Precision**: Quantities use DECIMAL(8,3) for precise measurements
5. **Enumerated Values**: Status fields limited to predefined values

### Performance Considerations
1. **Indexing Strategy**: Indexes on foreign keys and frequently queried columns
2. **Query Optimization**: Composite indexes for common query patterns
3. **Data Archiving**: Audit logs archived after 1 year
4. **Soft Deletes**: Important entities use `is_active` flags instead of hard deletes
5. **Pagination**: Large result sets paginated to improve response times

## Migration Strategy

### Initial Setup
1. Create core tables: `users`, `groups`, `group_members`
2. Add reference tables: `categories`, `units`
3. Create main functionality: `foods`, `fridge_items`, `shopping_lists`, `shopping_tasks`

### Phase 2 Extensions
1. Add meal planning: `meal_plans`, `meal_plan_items`
2. Implement recipes: `recipes`, `recipe_steps`
3. Add audit logging: `audit_logs`

### Data Seeding
1. **System Categories**: Default food categories (Vegetables, Fruits, Dairy, etc.)
2. **System Units**: Common measurement units (kg, g, l, ml, pieces, etc.)
3. **Demo Data**: Sample foods and recipes for testing

This data model provides a solid foundation for the food management platform while maintaining flexibility for future enhancements and scalability requirements.