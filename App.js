
import { StatusBar } from 'expo-status-bar';
import React, { useState,useEffect, useRef } from "react"; 
import {Platform,StyleSheet,Button,Text,Image, View, Alert ,TouchableOpacity} from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import {IconButton } from "@react-native-material/core";
import Icon from "@expo/vector-icons/MaterialCommunityIcons";
import busImage from './assets/pngwing.com2.png'
import axios from 'axios';

import {
  Provider,
  
  Dialog,
  DialogHeader,
  DialogContent,
  DialogActions,
  
} from "@react-native-material/core";
import * as Device from 'expo-device';
import * as Notifications from 'expo-notifications';


Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: false,
    shouldSetBadge: false,
  }),
});

const App = () => {
  const _mapView = React.createRef();
  const [visible, setVisible] = useState(false);
  const [expoPushToken, setExpoPushToken] = useState('');
  const [notification, setNotification] = useState(false);
  const [currentLocation,setCurrentLocation] = useState({
              latitude: 37.552369388104445, 
              longitude: 127.07333331532686,
              latitudeDelta: 0.003,
              longitudeDelta: 0.003
  });
  const notificationListener = useRef();
  const responseListener = useRef();
  const url = 'http://20.194.63.168:5000'
  function target1() {
    _mapView.current.animateToRegion(currentLocation, 1500);
        axios.get(`${url}/?sid=10`).then((res) => {
          console.log("gps =",res.data);
        })
    
  }
  useEffect(() => {
    registerForPushNotificationsAsync().then(token => setExpoPushToken(token));
    

    notificationListener.current = Notifications.addNotificationReceivedListener(notification => {
      setNotification(notification);
    });

    responseListener.current = Notifications.addNotificationResponseReceivedListener(response => {
      console.log(response);
    });

    return () => {
      Notifications.removeNotificationSubscription(notificationListener.current);
      Notifications.removeNotificationSubscription(responseListener.current);
    };
  }, []);
  console.log(notification)
  useEffect(() => {
    axios.post(`${url}/token`,{
      token: expoPushToken
    }).then(res => {
        console.log("token =",res.data)
    }).catch((err) => {
      console.log("token 보내기 실패");
    })
  },[expoPushToken])
  useEffect(() =>{
    setTimeout(() => {
      axios.get(`${url}/?sid=10`).then((res) => {
        console.log("gps =",parseFloat(res.data.student.latitude))
        setCurrentLocation({
          latitude: parseFloat(res.data.student.latitude), 
          longitude: parseFloat(res.data.student.longitude),
          latitudeDelta: 0.003,
          longitudeDelta: 0.003
      })
      })

    }, 15000);
    
  } ,[currentLocation])
  async function registerForPushNotificationsAsync() {
    let token;
  
    if (Platform.OS === 'android') {
      await Notifications.setNotificationChannelAsync('default', {
        name: 'default',
        importance: Notifications.AndroidImportance.MAX,
        vibrationPattern: [0, 250, 250, 250],
        lightColor: '#FF231F7C',
      });
    }
  
    if (Device.isDevice) {
      const { status: existingStatus } = await Notifications.getPermissionsAsync();
      let finalStatus = existingStatus;
      if (existingStatus !== 'granted') {
        const { status } = await Notifications.requestPermissionsAsync();
        finalStatus = status;
      }
      if (finalStatus !== 'granted') {
        alert('Failed to get push token for push notification!');
        return;
      }
      token = (await Notifications.getExpoPushTokenAsync()).data;
      console.log(token);
    } else {
      alert('Must use physical device for Push Notifications');
    }
  
    return token;
  }
    
  return (
    <View style={styles.container}>
      <StatusBar style="auto" />
      <Dialog visible={visible} onDismiss={() => setVisible(false)}>
        <DialogHeader title="알림을 보여줄게요" />
        <DialogContent>
          <Text>
            {`알림 1\n알림 2\n알림 3\n알림 4\n알림 5\n알림 6\n알림 7`}
          </Text>
        </DialogContent>
        <DialogActions>
         
          <Button
            title="Ok"
            compact
            variant="text"
            onPress={() => setVisible(false)}
          />
        </DialogActions>
      </Dialog>
      <View style={styles.header}>
        <Text style={styles.btnText}>Smart Bus</Text>
      </View>
      <View style={styles.contents}>
        <View style={styles.button}>
        <Button
          title = "알림 확인"
          onPress={() => setVisible(true)} 
          style = {styles.button}
        />
        </View>
      </View>
      <View style={styles.frame}>
        <View style ={styles.container2}>
        <MapView
        ref={_mapView }
          style={styles.map}
          initialRegion={
            {
              latitude: 37.552369388104445, 
              longitude: 127.07333331532686,
              latitudeDelta: 0.003,
              longitudeDelta: 0.003
            }
          }
          
          
          //add marker when user presses and hold map
            
            
        >
           <Marker style={styles.marker}
              coordinate={currentLocation}
              image={busImage}
              centerOffset={{x:0,y:0}}
              title="this is a marker"
              description="this is a marker example"
            />
            
            </MapView>
        
      </View>
      </View>
     <View>
        <IconButton onPress={target1} icon={props => <Icon name="crosshairs-gps" {...props} />} />
        
      </View>
      {/* <View
      style={{
        flex: 1,
        alignItems: 'center',
        justifyContent: 'space-around',
      }}>
      <Text>Your expo push token: {expoPushToken}</Text> 
       <View style={{ alignItems: 'center', justifyContent: 'center' }}>
        <Text>Title: {notification && notification.request.content.title} </Text>
        <Text>Body: {notification && notification.request.content.body}</Text>
        <Text>Data: {notification && JSON.stringify(notification.request.content.data)}</Text>
      </View>
    </View>  */}
    </View>
  );
  
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor : "#f2f2f2",
    paddingHorizontal: 20,
  },
  header: {
    justifyContent: "space-between",
    flexDirection :"row",
    marginTop: 100,
    
  },
  contents: {
    flexDirection : "column",
    marginTop: 50,
    
  },
  btnText:{
    fontSize: 38,
    fontWeight: "600",
    color : "black",
  },
  button:{
    borderStyle: 'solid',
    backgroundColor: 'white',
    shadowColor: "#000000",
    shadowOpacity: 0.3,
    shadowOffset: {width:2, height : 2},
    borderRadius : '8%',
    
  },
  frame:{
    flex:0.8,
    
    marginTop: 10
  },
  container2: {
    ...StyleSheet.absoluteFillObject,
    
    flex: 1,
  },
  map: {
    ...StyleSheet.absoluteFillObject,
    borderRadius : '8%',
  },
  marker:{
    width:'2%',
    height:'2%',
  }
});
const AppProvider = () => (
  <Provider>
    <App />
  </Provider>
);
export default AppProvider;
