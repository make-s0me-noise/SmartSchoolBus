
import { StatusBar } from 'expo-status-bar';
import React, { useState } from "react"; 
import {StyleSheet,Button,Text,Image, View, Alert ,TouchableOpacity} from 'react-native';
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

const App = () => {
  const _mapView = React.createRef();
  const [visible, setVisible] = useState(false);
  function target1() {
    _mapView.current.animateToRegion({latitude: 37.532600,
      longitude: 127.024612,
      latitudeDelta: 0.003,
      longitudeDelta: 0.003
        }, 2000);
    
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
