// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./safeMath.sol";

contract WavePortal {

    using SafeMath for uint;

    address public admin;

    mapping(address => string) public waveRoomId;
    mapping(string => string) public roomTopic;
    mapping(string => bool) public isTaken;

    mapping(string => address[]) public waveRoomMembers; // this will need to be an array implemented with permissions

    event waveRoomCreated(address _createdBy, string _waveRoomId);
    event waveRoomIdChanged(address _owner, string _oldRoomId, string _newRoomId);
    event roomTopicChanged(address _owner, string _oldTopic, string _newTopic);

    constructor() {
        admin = msg.sender;
    }

    function createRoom(string memory _waveRoomId, string memory _waveRoomTopic) public returns (bool success) {
        require(isTaken[_waveRoomId] == false, "Pick a different Wave Room ID");

        isTaken[_waveRoomId] = true;
        waveRoomId[msg.sender] = _waveRoomId;

        roomTopic[_waveRoomId] = _waveRoomTopic;

        emit waveRoomCreated(msg.sender, _waveRoomId);
        return true;
    }
    
    function changeRoomId(string memory _newRoomId) public returns (bool success) {
        require(isTaken[_newRoomId] == false);
        string memory _oldRoomId = waveRoomId[msg.sender];
        waveRoomId[msg.sender] = _newRoomId;
        emit waveRoomIdChanged(msg.sender, _oldRoomId, _newRoomId);
        return true;
    }

    function changeRoomTopic(string memory _roomId, string memory _newTopic) public returns (bool success) {
        require(keccak256(abi.encodePacked(waveRoomId[msg.sender])) == keccak256(abi.encodePacked(_roomId)), "Enter correct room id");
        string memory _oldTopic = roomTopic[_roomId];
        roomTopic[_roomId] = _newTopic;
        emit roomTopicChanged(msg.sender, _oldTopic, roomTopic[_roomId]);
        return true;
    }

    // could also use open zepplin only owner function modifiers
    function addMembers(string memory _roomId, address _newMember) public returns (bool success) {
        require(keccak256(abi.encodePacked(waveRoomId[msg.sender])) == keccak256(abi.encodePacked(_roomId)), "Enter correct room id");

        waveRoomMembers[_roomId].push(_newMember);
        return true;
    }
}