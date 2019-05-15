-- Create schema
create schema if not exists SoftwareEngineeringProject;

use SoftwareEngineeringProject;

-- Create tables
create table if not exists Cities_Cities
(
    city_id       int          not null auto_increment,
    country_name  nvarchar(20) not null,
    province_name nvarchar(20) not null,
    city_name     nvarchar(20) not null,
    latitude      float        not null,
    longitude     float        not null,

    -- clustered index
    constraint PK_Cities
        primary key (city_id, country_name, province_name, city_name)
);

create table if not exists Users_Users
(
    user_id          int                 not null auto_increment,
    user_name        nvarchar(20)        not null,
    pswd_hash        char(16)            not null,
    email            varchar(25)         not null unique,
    gender           char(1) default 'U' not null,
    resident_city_id int                 not null,

    -- clustered index
    constraint PK_Users
        primary key (user_id, email),

    constraint FK_Users_Cities
        foreign key (resident_city_id)
            references Cities (city_id),
    constraint CHK_Email
        check (email like '%@%'),
    constraint CHK_Gender
        check (gender in ('M', -- male
                          'F', -- female
                          'O', -- other
                          'U'  -- unknown
            ))
);

create table if not exists Users_FriendRelations
(
    user_id          int not null,
    friend_user_id   int not null,
    friend_user_note nvarchar(20),

    -- clustered index
    constraint PK_FriendRelations
        primary key (user_id, friend_user_id),

    constraint FK_FriendRelations_User
        foreign key (user_id)
            references Users (user_id),
    constraint FK_FriendRelations_Friend
        foreign key (friend_user_id)
            references Users (user_id)
);

create table if not exists Travels_TravelGroups
(
    travel_groups_id   int           not null auto_increment,
    travel_groups_note nvarchar(140) not null,

    -- clustered index
    constraint PK_TravelGroups
        primary key (travel_groups_id)
);

create table if not exists Travels_TravelGroupOwnership
(
    user_id          int not null,
    travel_groups_id int not null,

    -- clustered index
    constraint PK_TravelGroupOwnership
        primary key (user_id, travel_groups_id),

    constraint FK_TravelGroupOwnership_Users
        foreign key (user_id)
            references Users (user_id),
    constraint FK_TravelGroupOwnership_TravelGroups
        foreign key (travel_groups_id)
            references TravelGroups (travel_groups_id)
);

create table if not exists Travels_Travels
(
    travel_id   int                 not null auto_increment,
    date_start  date                not null,
    date_end    date                not null,
    city_id     int                 not null,
    visibility  char(1) default 'F' not null,
    travel_note nvarchar(140)       not null,

    -- clustered index
    constraint PK_Travels
        primary key (travel_id),

    constraint FK_Travels_Cities
        foreign key (city_id)
            references Cities (city_id),
    constraint CHK_Visibility
        check (visibility in ('M', -- only me
                              'F', -- friends
                              'P'  -- public
            ))
);

alter table Travels_Travels
    add index (date_start, date_end);
alter table Travels_Travels
    add index (city_id);

create table if not exists Travels_TravelGrouping
(
    travel_id        int not null,
    travel_groups_id int not null,

    -- clustered index
    constraint PK_TravelGrouping
        primary key (travel_id, travel_groups_id),

    constraint FK_TravelGrouping_Travels
        foreign key (travel_id)
            references Travels (travel_id),
    constraint FK_TravelGrouping_TravelGroups
        foreign key (travel_groups_id)
            references TravelGroups (travel_groups_id)
);

create table if not exists Travels_TravelAssociation
(
    travel_id       int not null,
    company_user_id int not null,

    -- clustered index
    constraint PK_TravelAssociation
        primary key (travel_id),

    constraint FK_TravelAssociation_Travels
        foreign key (travel_id)
            references Travels (travel_id),
    constraint FK_TravelAssociation_Users
        foreign key (company_user_id)
            references Users (user_id)
);

create table if not exists Messages_FriendRequests
(
    msg_id         int                 not null auto_increment,
    user_id        int                 not null,
    friend_user_id int                 not null,
    msg_type       char(1) default 'A' not null,
    msg_content    nvarchar(140)       not null,

    -- clustered index
    constraint PK_FriendRequests
        primary key (msg_id, user_id),

    constraint FK_FriendRequests_User
        foreign key (user_id)
            references Users (user_id),
    constraint FK_FriendRequests_Friend
        foreign key (friend_user_id)
            references Users (user_id),
    constraint CHK_FriendRequests_Msg_Type
        check (msg_type in ('A', -- add
                            'D'  -- delete
            ))
);

create table if not exists Messages_TravelAssociation
(
    msg_id         int           not null auto_increment,
    user_id        int           not null,
    friend_user_id int           not null,
    travel_id      int           not null,
    msg_type       char(1)       not null,
    msg_content    nvarchar(140) not null,

    -- clustered index
    constraint PK_TravelAssociation
        primary key (msg_id, user_id),

    constraint FK_TravelAssociation_User
        foreign key (user_id)
            references Users (user_id),
    constraint FK_TravelAssociation_Friend
        foreign key (friend_user_id)
            references Users (user_id),
    constraint CHK_TravelAssociation_Msg_Type
        check (msg_type in ('I', -- invite
                            'A', -- add
                            'L', -- leave
                            'M', -- modify
                            'D'  -- delete
            ))
);
