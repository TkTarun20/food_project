insert into
  food_store_category (id, title)
values
  (1, 'Snacks'),
  (2, 'Chinese'),
  (3, 'South Indian'),
  (4, 'Soup'),
  (5, 'Shakes');

insert into
  food_store_fooditem (
    id,
    title,
    description,
    slug,
    type,
    unit_price,
    last_update,
    category_id
  )
values
  (
    1,
    'Sandwich',
    'mus vivamus vestibulum sagittis sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus.',
    '-',
    'V',
    69,
    '2022-04-16 00:00:00',
    1
  ),
  (
    2,
    'Cheese Sandwich',
    'maecenas tincidunt lacus at velit vivamus vel nulla eget eros elementum pellentesque.',
    '',
    'V',
    81,
    '2022-04-10 00:00:00',
    1
  ),
  (
    3,
    'Hakka Noodles',
    'nisi volutpat eleifend donec ut dolor morbi vel lectus in quam.',
    '-',
    'NV',
    96,
    '2022-04-5 00:00:00',
    2
  ),
  (
    4,
    'Schezwan Fried Rice',
    'posuere cubilia curae nulla dapibus dolor vel est donec odio justo sollicitudin ut.',
    '',
    'V',
    98,
    '2022-03-2 00:00:00',
    2
  ),
  (
    5,
    'Paneer Masala Dosa',
    'lectus in est risus auctor sed tristique in tempus sit amet sem fusce consequat nulla nisl nunc.',
    '-',
    'V',
    115,
    '2022-01-30 00:00:00',
    3
  ),
  (
    6,
    'Idli Sambhar',
    '4 delicious idlis with nariyal chutney.',
    '-',
    'V',
    46,
    '2022-01-10 00:00:00',
    3
  ),
  (
    7,
    'Mysore Masala Dosa',
    'Special Mysori dosa with hari chutney.',
    '-',
    'V',
    92,
    '2022-02-7 00:00:00',
    3
  ),
  (
    8,
    'Hot & Sour Soup',
    'A special and delicious hot drink for winters.',
    '-',
    'V',
    45,
    '2022-06-08 17:14:22',
    4
  ),
  (
    9,
    'Paneer Burger',
    'lorem ipsum generator',
    '-',
    'V',
    92,
    '2022-06-05 00:00:00',
    1
  ),
  (
    10,
    'Paneer Cheese Burger',
    'Paneer Burger with cheese fillings.',
    '-',
    'V',
    104,
    '2022-06-06 00:00:00',
    1
  ),
  (
    11,
    'Tomato Soup',
    'Special Mysori dosa with hari chutney.',
    '-',
    'V',
    40,
    '2022-02-7 00:00:00',
    4
  ),
  (
    12,
    'Veg Combi',
    'lorem uosm gentr.',
    '-',
    'V',
    80,
    '2022-07-09 17:51:11',
    2
  ),
  (
    13,
    'Chilli Paneer',
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    '-',
    'V',
    150,
    '2022-07-09 17:20:11',
    2
  ),
  (
    14,
    'Hot Chocolate Oreo Shake',
    'Chilled Chocolate milk with fillings of oreo biscuits.',
    '-',
    'V',
    120,
    '2022-08-04 14:03:46',
    5
  );