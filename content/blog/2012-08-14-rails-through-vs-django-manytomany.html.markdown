Title: "Rails 'through' vs Django 'ManyToMany'"
Tags: [Django, Ruby on Rails]

Ok, Rails & company have a lot of great points--I love RSpec--but I've noticed a few areas where Rails can improve.  Here, namely, I see a big difference in handling multiple relationships to self.

## In Rails

``db/migrate/create_relationships.rb``

```ruby
class CreateRelationships < ActiveRecord::Migration
    def change
        create_table :relationships do |t|
            t.integer :person_id
            t.integer :friend_id
            t.timestamps
        end

        add_index :relationships, :person_id
        add_index :relationships, :friend_id
        add_index :relationships, [:person_id, :friend_id], unique: true
    end
end
```

``app/models/relationship.rb``

```ruby
class Relationship < ActiveRecord::Base
    attr_accessible :friend_id

    belongs_to :person, class_name: "Person"
    belongs_to :friend, class_name: "Person"
end
```

``app/models/person.rb``

```ruby
class Person < ActiveRecord::Base
    has_many :relationships, foreign_key: "person_id"
    has_many :friends, through: :relationships, source: :friend
end
```

## In Django

``people/models.py``

```python
class Person(models.Model):
    friends = models.ManyToManyField('self')
```

I think there's a clear winner here--to quote from the [tutorial][1] I'm following:

> We begin with the tests, having faith that the magic of Rails will come to the rescue.

[1]: http://ruby.railstutorial.org/
