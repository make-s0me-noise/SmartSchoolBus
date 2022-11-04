
import { StatusBar } from 'expo-status-bar';
import React, { useState,useEffect, useRef } from "react"; 
import {Platform,StyleSheet,Button,Text,Image, View, Alert ,TouchableOpacity} from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import {IconButton } from "@react-native-material/core";
import Icon from "@expo/vector-icons/MaterialCommunityIcons";
import busImage from './assets/pngwing.com2.png'
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
  const notificationListener = useRef();
  const responseListener = useRef();
  function target1() {
    _mapView.current.animateToRegion({latitude: 37.532600,
      longitude: 127.024612,
      latitudeDelta: 0.003,
      longitudeDelta: 0.003
        }, 2000);
    
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
  //console.log(notification)

  async function schedulePushNotification() {
    await Notifications.scheduleNotificationAsync({
      content: {
        title: "You've got mail! 📬",
        body: 'Here is the notification body',
        data: { data: 'goes here' },
      },
      trigger: { seconds: 2 },
    });
  }
  
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
          region={
            {latitude: 37.532600, longitude: 127.024612}
          }
          
          
          //add marker when user presses and hold map
            
            
        >
           <Marker style={styles.marker}
              coordinate={{latitude: 37.532600, longitude: 127.024612}}
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
      <View
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
      <Button
        title="Press to schedule a notification"
        onPress={async () => {
          await schedulePushNotification();
        }}
      />
    </View> 
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
