# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modernart.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='modernart.proto',
  package='',
  serialized_pb=_b('\n\x0fmodernart.proto\"U\n\x06\x41rtist\"K\n\x02Id\x12\x0e\n\nLITE_METAL\x10\x01\x12\x08\n\x04YOKO\x10\x02\x12\x0e\n\nCHRISTIN_P\x10\x03\x12\x0f\n\x0bKARL_GITTER\x10\x04\x12\n\n\x06KRYPTO\x10\x05\"Q\n\x0b\x41uctionType\"B\n\x02Id\x12\n\n\x06SEALED\x10\x01\x12\t\n\x05\x46IXED\x10\x02\x12\x0f\n\x0bONCE_AROUND\x10\x03\x12\x08\n\x04OPEN\x10\x04\x12\n\n\x06\x44OUBLE\x10\x05\"I\n\x04\x43\x61rd\x12\x1a\n\x06\x61rtist\x18\x01 \x02(\x0e\x32\n.Artist.Id\x12%\n\x0c\x61uction_type\x18\x02 \x02(\x0e\x32\x0f.AuctionType.Id\"\\\n\x0ePlayerHoldings\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\r\n\x05money\x18\x02 \x02(\r\x12\x13\n\x04hand\x18\x03 \x03(\x0b\x32\x05.Card\x12\x18\n\tpurchases\x18\x04 \x03(\x0b\x32\x05.Card\"s\n\x07\x41uction\x12\x14\n\x05\x63\x61rds\x18\x01 \x03(\x0b\x32\x05.Card\x12\x14\n\x0cseller_names\x18\x02 \x03(\t\x12\x12\n\nends_round\x18\x03 \x01(\x08\x12\x13\n\x0bwinning_bid\x18\x04 \x01(\r\x12\x13\n\x0bwinner_name\x18\x05 \x01(\t\"\x89\x02\n\x05\x42oard\x12\x13\n\x04\x64\x65\x63k\x18\x01 \x03(\x0b\x32\x05.Card\x12\x19\n\x07\x61uction\x18\x02 \x01(\x0b\x32\x08.Auction\x12+\n\x0eround_outcomes\x18\x03 \x03(\x0b\x32\x13.Board.RoundOutcome\x12(\n\x0fplayer_holdings\x18\x04 \x03(\x0b\x32\x0f.PlayerHoldings\x1a:\n\rArtistOutcome\x12\x1a\n\x06\x61rtist\x18\x01 \x02(\x0e\x32\n.Artist.Id\x12\r\n\x05value\x18\x02 \x02(\r\x1a=\n\x0cRoundOutcome\x12-\n\x0f\x61rtist_outcomes\x18\x01 \x03(\x0b\x32\x14.Board.ArtistOutcome\"5\n\nPlayerJoin\x12\x13\n\x0bplayer_name\x18\x01 \x02(\t\x12\x12\n\nplay_order\x18\x02 \x02(\r\"\"\n\nRoundStart\x12\x14\n\x0cround_number\x18\x01 \x02(\r\")\n\x0c\x41uctionStart\x12\x19\n\x07\x61uction\x18\x01 \x02(\x0b\x32\x08.Auction\"B\n\x03\x42id\x12\x19\n\x07\x61uction\x18\x01 \x02(\x0b\x32\x08.Auction\x12\x13\n\x0bplayer_name\x18\x02 \x02(\t\x12\x0b\n\x03\x62id\x18\x03 \x01(\r\"\'\n\nAuctionEnd\x12\x19\n\x07\x61uction\x18\x01 \x02(\x0b\x32\x08.Auction\"Q\n\x08RoundEnd\x12\x19\n\x07\x61uction\x18\x01 \x02(\x0b\x32\x08.Auction\x12*\n\rround_outcome\x18\x02 \x02(\x0b\x32\x13.Board.RoundOutcome\"M\n\x07Payment\x12\r\n\x05payor\x18\x01 \x01(\t\x12\r\n\x05payee\x18\x02 \x01(\t\x12\x0e\n\x06\x61mount\x18\x03 \x02(\r\x12\x14\n\x05\x63\x61rds\x18\x04 \x03(\x0b\x32\x05.Card\"\x82\x01\n\x07GameEnd\x12/\n\x0fplayer_outcomes\x18\x01 \x03(\x0b\x32\x16.GameEnd.PlayerOutcome\x1a\x46\n\rPlayerOutcome\x12\x13\n\x0bplayer_name\x18\x01 \x02(\t\x12\r\n\x05money\x18\x02 \x02(\r\x12\x11\n\tis_winner\x18\x03 \x02(\x08')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_ARTIST_ID = _descriptor.EnumDescriptor(
  name='Id',
  full_name='Artist.Id',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LITE_METAL', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='YOKO', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHRISTIN_P', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='KARL_GITTER', index=3, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='KRYPTO', index=4, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=29,
  serialized_end=104,
)
_sym_db.RegisterEnumDescriptor(_ARTIST_ID)

_AUCTIONTYPE_ID = _descriptor.EnumDescriptor(
  name='Id',
  full_name='AuctionType.Id',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SEALED', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIXED', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ONCE_AROUND', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPEN', index=3, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DOUBLE', index=4, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=121,
  serialized_end=187,
)
_sym_db.RegisterEnumDescriptor(_AUCTIONTYPE_ID)


_ARTIST = _descriptor.Descriptor(
  name='Artist',
  full_name='Artist',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ARTIST_ID,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=104,
)


_AUCTIONTYPE = _descriptor.Descriptor(
  name='AuctionType',
  full_name='AuctionType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _AUCTIONTYPE_ID,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=106,
  serialized_end=187,
)


_CARD = _descriptor.Descriptor(
  name='Card',
  full_name='Card',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='artist', full_name='Card.artist', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='auction_type', full_name='Card.auction_type', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=189,
  serialized_end=262,
)


_PLAYERHOLDINGS = _descriptor.Descriptor(
  name='PlayerHoldings',
  full_name='PlayerHoldings',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='PlayerHoldings.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='money', full_name='PlayerHoldings.money', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='hand', full_name='PlayerHoldings.hand', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='purchases', full_name='PlayerHoldings.purchases', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=264,
  serialized_end=356,
)


_AUCTION = _descriptor.Descriptor(
  name='Auction',
  full_name='Auction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cards', full_name='Auction.cards', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seller_names', full_name='Auction.seller_names', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ends_round', full_name='Auction.ends_round', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='winning_bid', full_name='Auction.winning_bid', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='winner_name', full_name='Auction.winner_name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=358,
  serialized_end=473,
)


_BOARD_ARTISTOUTCOME = _descriptor.Descriptor(
  name='ArtistOutcome',
  full_name='Board.ArtistOutcome',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='artist', full_name='Board.ArtistOutcome.artist', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='Board.ArtistOutcome.value', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=620,
  serialized_end=678,
)

_BOARD_ROUNDOUTCOME = _descriptor.Descriptor(
  name='RoundOutcome',
  full_name='Board.RoundOutcome',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='artist_outcomes', full_name='Board.RoundOutcome.artist_outcomes', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=680,
  serialized_end=741,
)

_BOARD = _descriptor.Descriptor(
  name='Board',
  full_name='Board',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deck', full_name='Board.deck', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='auction', full_name='Board.auction', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='round_outcomes', full_name='Board.round_outcomes', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='player_holdings', full_name='Board.player_holdings', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_BOARD_ARTISTOUTCOME, _BOARD_ROUNDOUTCOME, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=476,
  serialized_end=741,
)


_PLAYERJOIN = _descriptor.Descriptor(
  name='PlayerJoin',
  full_name='PlayerJoin',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_name', full_name='PlayerJoin.player_name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='play_order', full_name='PlayerJoin.play_order', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=743,
  serialized_end=796,
)


_ROUNDSTART = _descriptor.Descriptor(
  name='RoundStart',
  full_name='RoundStart',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='round_number', full_name='RoundStart.round_number', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=798,
  serialized_end=832,
)


_AUCTIONSTART = _descriptor.Descriptor(
  name='AuctionStart',
  full_name='AuctionStart',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auction', full_name='AuctionStart.auction', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=834,
  serialized_end=875,
)


_BID = _descriptor.Descriptor(
  name='Bid',
  full_name='Bid',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auction', full_name='Bid.auction', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='player_name', full_name='Bid.player_name', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bid', full_name='Bid.bid', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=877,
  serialized_end=943,
)


_AUCTIONEND = _descriptor.Descriptor(
  name='AuctionEnd',
  full_name='AuctionEnd',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auction', full_name='AuctionEnd.auction', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=945,
  serialized_end=984,
)


_ROUNDEND = _descriptor.Descriptor(
  name='RoundEnd',
  full_name='RoundEnd',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='auction', full_name='RoundEnd.auction', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='round_outcome', full_name='RoundEnd.round_outcome', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=986,
  serialized_end=1067,
)


_PAYMENT = _descriptor.Descriptor(
  name='Payment',
  full_name='Payment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='payor', full_name='Payment.payor', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payee', full_name='Payment.payee', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='amount', full_name='Payment.amount', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cards', full_name='Payment.cards', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1069,
  serialized_end=1146,
)


_GAMEEND_PLAYEROUTCOME = _descriptor.Descriptor(
  name='PlayerOutcome',
  full_name='GameEnd.PlayerOutcome',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_name', full_name='GameEnd.PlayerOutcome.player_name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='money', full_name='GameEnd.PlayerOutcome.money', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_winner', full_name='GameEnd.PlayerOutcome.is_winner', index=2,
      number=3, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1209,
  serialized_end=1279,
)

_GAMEEND = _descriptor.Descriptor(
  name='GameEnd',
  full_name='GameEnd',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_outcomes', full_name='GameEnd.player_outcomes', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_GAMEEND_PLAYEROUTCOME, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1149,
  serialized_end=1279,
)

_ARTIST_ID.containing_type = _ARTIST
_AUCTIONTYPE_ID.containing_type = _AUCTIONTYPE
_CARD.fields_by_name['artist'].enum_type = _ARTIST_ID
_CARD.fields_by_name['auction_type'].enum_type = _AUCTIONTYPE_ID
_PLAYERHOLDINGS.fields_by_name['hand'].message_type = _CARD
_PLAYERHOLDINGS.fields_by_name['purchases'].message_type = _CARD
_AUCTION.fields_by_name['cards'].message_type = _CARD
_BOARD_ARTISTOUTCOME.fields_by_name['artist'].enum_type = _ARTIST_ID
_BOARD_ARTISTOUTCOME.containing_type = _BOARD
_BOARD_ROUNDOUTCOME.fields_by_name['artist_outcomes'].message_type = _BOARD_ARTISTOUTCOME
_BOARD_ROUNDOUTCOME.containing_type = _BOARD
_BOARD.fields_by_name['deck'].message_type = _CARD
_BOARD.fields_by_name['auction'].message_type = _AUCTION
_BOARD.fields_by_name['round_outcomes'].message_type = _BOARD_ROUNDOUTCOME
_BOARD.fields_by_name['player_holdings'].message_type = _PLAYERHOLDINGS
_AUCTIONSTART.fields_by_name['auction'].message_type = _AUCTION
_BID.fields_by_name['auction'].message_type = _AUCTION
_AUCTIONEND.fields_by_name['auction'].message_type = _AUCTION
_ROUNDEND.fields_by_name['auction'].message_type = _AUCTION
_ROUNDEND.fields_by_name['round_outcome'].message_type = _BOARD_ROUNDOUTCOME
_PAYMENT.fields_by_name['cards'].message_type = _CARD
_GAMEEND_PLAYEROUTCOME.containing_type = _GAMEEND
_GAMEEND.fields_by_name['player_outcomes'].message_type = _GAMEEND_PLAYEROUTCOME
DESCRIPTOR.message_types_by_name['Artist'] = _ARTIST
DESCRIPTOR.message_types_by_name['AuctionType'] = _AUCTIONTYPE
DESCRIPTOR.message_types_by_name['Card'] = _CARD
DESCRIPTOR.message_types_by_name['PlayerHoldings'] = _PLAYERHOLDINGS
DESCRIPTOR.message_types_by_name['Auction'] = _AUCTION
DESCRIPTOR.message_types_by_name['Board'] = _BOARD
DESCRIPTOR.message_types_by_name['PlayerJoin'] = _PLAYERJOIN
DESCRIPTOR.message_types_by_name['RoundStart'] = _ROUNDSTART
DESCRIPTOR.message_types_by_name['AuctionStart'] = _AUCTIONSTART
DESCRIPTOR.message_types_by_name['Bid'] = _BID
DESCRIPTOR.message_types_by_name['AuctionEnd'] = _AUCTIONEND
DESCRIPTOR.message_types_by_name['RoundEnd'] = _ROUNDEND
DESCRIPTOR.message_types_by_name['Payment'] = _PAYMENT
DESCRIPTOR.message_types_by_name['GameEnd'] = _GAMEEND

Artist = _reflection.GeneratedProtocolMessageType('Artist', (_message.Message,), dict(
  DESCRIPTOR = _ARTIST,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:Artist)
  ))
_sym_db.RegisterMessage(Artist)

AuctionType = _reflection.GeneratedProtocolMessageType('AuctionType', (_message.Message,), dict(
  DESCRIPTOR = _AUCTIONTYPE,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:AuctionType)
  ))
_sym_db.RegisterMessage(AuctionType)

Card = _reflection.GeneratedProtocolMessageType('Card', (_message.Message,), dict(
  DESCRIPTOR = _CARD,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:Card)
  ))
_sym_db.RegisterMessage(Card)

PlayerHoldings = _reflection.GeneratedProtocolMessageType('PlayerHoldings', (_message.Message,), dict(
  DESCRIPTOR = _PLAYERHOLDINGS,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:PlayerHoldings)
  ))
_sym_db.RegisterMessage(PlayerHoldings)

Auction = _reflection.GeneratedProtocolMessageType('Auction', (_message.Message,), dict(
  DESCRIPTOR = _AUCTION,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:Auction)
  ))
_sym_db.RegisterMessage(Auction)

Board = _reflection.GeneratedProtocolMessageType('Board', (_message.Message,), dict(

  ArtistOutcome = _reflection.GeneratedProtocolMessageType('ArtistOutcome', (_message.Message,), dict(
    DESCRIPTOR = _BOARD_ARTISTOUTCOME,
    __module__ = 'modernart_pb2'
    # @@protoc_insertion_point(class_scope:Board.ArtistOutcome)
    ))
  ,

  RoundOutcome = _reflection.GeneratedProtocolMessageType('RoundOutcome', (_message.Message,), dict(
    DESCRIPTOR = _BOARD_ROUNDOUTCOME,
    __module__ = 'modernart_pb2'
    # @@protoc_insertion_point(class_scope:Board.RoundOutcome)
    ))
  ,
  DESCRIPTOR = _BOARD,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:Board)
  ))
_sym_db.RegisterMessage(Board)
_sym_db.RegisterMessage(Board.ArtistOutcome)
_sym_db.RegisterMessage(Board.RoundOutcome)

PlayerJoin = _reflection.GeneratedProtocolMessageType('PlayerJoin', (_message.Message,), dict(
  DESCRIPTOR = _PLAYERJOIN,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:PlayerJoin)
  ))
_sym_db.RegisterMessage(PlayerJoin)

RoundStart = _reflection.GeneratedProtocolMessageType('RoundStart', (_message.Message,), dict(
  DESCRIPTOR = _ROUNDSTART,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:RoundStart)
  ))
_sym_db.RegisterMessage(RoundStart)

AuctionStart = _reflection.GeneratedProtocolMessageType('AuctionStart', (_message.Message,), dict(
  DESCRIPTOR = _AUCTIONSTART,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:AuctionStart)
  ))
_sym_db.RegisterMessage(AuctionStart)

Bid = _reflection.GeneratedProtocolMessageType('Bid', (_message.Message,), dict(
  DESCRIPTOR = _BID,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:Bid)
  ))
_sym_db.RegisterMessage(Bid)

AuctionEnd = _reflection.GeneratedProtocolMessageType('AuctionEnd', (_message.Message,), dict(
  DESCRIPTOR = _AUCTIONEND,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:AuctionEnd)
  ))
_sym_db.RegisterMessage(AuctionEnd)

RoundEnd = _reflection.GeneratedProtocolMessageType('RoundEnd', (_message.Message,), dict(
  DESCRIPTOR = _ROUNDEND,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:RoundEnd)
  ))
_sym_db.RegisterMessage(RoundEnd)

Payment = _reflection.GeneratedProtocolMessageType('Payment', (_message.Message,), dict(
  DESCRIPTOR = _PAYMENT,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:Payment)
  ))
_sym_db.RegisterMessage(Payment)

GameEnd = _reflection.GeneratedProtocolMessageType('GameEnd', (_message.Message,), dict(

  PlayerOutcome = _reflection.GeneratedProtocolMessageType('PlayerOutcome', (_message.Message,), dict(
    DESCRIPTOR = _GAMEEND_PLAYEROUTCOME,
    __module__ = 'modernart_pb2'
    # @@protoc_insertion_point(class_scope:GameEnd.PlayerOutcome)
    ))
  ,
  DESCRIPTOR = _GAMEEND,
  __module__ = 'modernart_pb2'
  # @@protoc_insertion_point(class_scope:GameEnd)
  ))
_sym_db.RegisterMessage(GameEnd)
_sym_db.RegisterMessage(GameEnd.PlayerOutcome)


# @@protoc_insertion_point(module_scope)
