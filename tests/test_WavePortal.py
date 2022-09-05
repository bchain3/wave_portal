import brownie

# checks on one address only having one room will be managed in front end to prevent gas consumption

def test_checkAdmin(wavePortal, accounts):
    assert wavePortal.admin() == accounts[0]


def test_room_creation_event_fires(wavePortal, accounts):
    tx = wavePortal.createRoom('myRoom', 'myTopic', {'from':accounts[0]})

    assert len(tx.events) == 1
    assert tx.events['waveRoomCreated'].values() == [accounts[0], 'myRoom']


def test_room_id_change_event_fires(wavePortal, accounts):
    _oldRoomId = 'myRoom'
    _newRoomId = 'myRoomNew'
    wavePortal.createRoom(_oldRoomId, 'myTopic', {'from':accounts[0]})

    tx = wavePortal.changeRoomId(_newRoomId, {'from':accounts[0]})

    assert len(tx.events) == 1
    assert tx.events['waveRoomIdChanged'].values() == [accounts[0], _oldRoomId, _newRoomId]


def test_room_creation_successful(wavePortal, accounts):
    roomId = 'RoomZero'
    tx = wavePortal.createRoom(roomId, 'myTopic', {'from':accounts[0]})

    assert tx.return_value is True


def test_room_creation_roomId_in_use(wavePortal, accounts):
    roomId = 'myRoom'
    wavePortal.createRoom(roomId, 'myTopic', {'from':accounts[0]})

    with brownie.reverts():
        wavePortal.createRoom(roomId, 'myTopic', {'from':accounts[1]})


def test_isTaken_updated_correctly(wavePortal, accounts):
    roomId = 'myRoom'
    initial_status = wavePortal.isTaken(roomId)

    wavePortal.createRoom(roomId, 'myTopic', {'from':accounts[0]})
    updated_status = wavePortal.isTaken(roomId)

    assert initial_status is False
    assert updated_status is True


def test_waveRoomId_updated_correctly(wavePortal, accounts):
    roomId = 'myRoom'
    initial_status = wavePortal.waveRoomId(accounts[0])

    wavePortal.createRoom(roomId, 'myTopic', {'from':accounts[0]})
    updated_status = wavePortal.waveRoomId(accounts[0])

    other_account_status = []

    for x in range(1,6):
        status = wavePortal.waveRoomId(accounts[x])
        other_account_status.append(status)

    assert initial_status == ''
    assert updated_status == roomId
    assert other_account_status == ['', '', '', '', '']


def test_changeRoomId_taken_name(wavePortal, accounts):
    wavePortal.createRoom('ZeroRoom', 'topicZero', {'from':accounts[0]})
    wavePortal.createRoom('OneRoom', 'topicOne', {'from':accounts[1]})

    with brownie.reverts(): #change this as no longer checking
        wavePortal.changeRoomId('OneRoom', {'from':accounts[0]})


def test_changeRoomId_successful(wavePortal, accounts):
    wavePortal.createRoom('myRoom', 'myTopic', {'from':accounts[0]})
    initial_value = wavePortal.waveRoomId(accounts[0])

    tx = wavePortal.changeRoomId('yourRoom', {'from':accounts[0]})
    updated_value = wavePortal.waveRoomId(accounts[0])

    assert initial_value == 'myRoom'
    assert updated_value == 'yourRoom'
    assert tx.return_value is True

# Function wise tests from her onwards    

def test_changeRoomTopic_successful(wavePortal, accounts):
    wavePortal.createRoom('myRoom', 'myTopic', {'from':accounts[0]})
    initial_topic = wavePortal.roomTopic('myRoom')

    wavePortal.changeRoomTopic('myRoom', 'yourTopic', {'from':accounts[0]})
    updated_topic = wavePortal.roomTopic('myRoom')

    assert initial_topic == 'myTopic'
    assert updated_topic == 'yourTopic'


def test_changeRoomTopic_incorrect_roomId_entered(wavePortal, accounts):
    wavePortal.createRoom('myRoom', 'myTopic', {'from':accounts[0]})

    with brownie.reverts():
        wavePortal.changeRoomTopic('yoMamaRoom', 'yoMamaTopic', {'from':accounts[0]})


def test_roomTopicChange_fires_correctly(wavePortal, accounts):
    wavePortal.createRoom('myRoom', 'myTopic', {'from':accounts[0]})

    tx = wavePortal.changeRoomTopic('myRoom', 'yourTopic', {'from':accounts[0]})
    
    assert len(tx.events) == 1
    assert tx.events['roomTopicChanged'].values() == [accounts[0], 'myTopic', 'yourTopic']