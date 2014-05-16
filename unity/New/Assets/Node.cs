using UnityEngine;
using System.Collections;

public class Node : MonoBehaviour {

    public Transform Led;
    public Transform Left;
    public Transform Right;
    public Transform Up;
    public Transform Down;
    public Transform Initiator;
    public int Id;
	// Use this for initialization
	void Start () {
       // LightOn();
	}
	
	// Update is called once per frame
	void Update () {


       
	}

    public void Walk() 
    {

        if (Initiator.GetComponent<Labirent>().direction == "Up" )
        {
            if (Up != null)
            {
                LightOff();
                Up.GetComponent<Node>().LightOn();
                Initiator.GetComponent<Labirent>().currentLed = Up;
            }
            else
            {
                Initiator.GetComponent<Labirent>().direction = Initiator.GetComponent<Keyboard>().Previous;
            }
        }
        else if (Initiator.GetComponent<Labirent>().direction == "Down" && Down!=null)
        {
             if (Down != null)
            {
            LightOff();
            Down.GetComponent<Node>().LightOn();
            Initiator.GetComponent<Labirent>().currentLed = Down;
             }
             else
             {
                 Initiator.GetComponent<Labirent>().direction = Initiator.GetComponent<Keyboard>().Previous;
             }
        }
        else if (Initiator.GetComponent<Labirent>().direction == "Left" && Left!=null)
        {
             if (Left != null)
             {
                LightOff();
                Left.GetComponent<Node>().LightOn();
                Initiator.GetComponent<Labirent>().currentLed = Left;
             }
             else
             {
                 Initiator.GetComponent<Labirent>().direction = Initiator.GetComponent<Keyboard>().Previous;
             }

        }
        else if (Initiator.GetComponent<Labirent>().direction == "Right" && Right != null)
        {
            if (Right != null)
            {
                LightOff();
                Right.GetComponent<Node>().LightOn();
                Initiator.GetComponent<Labirent>().currentLed = Right;
            }
            else
            {
                Initiator.GetComponent<Labirent>().direction = Initiator.GetComponent<Keyboard>().Previous;
            }
        }
       
    }


    void LightOn()
    {
        transform.GetComponent<MeshRenderer>().material.color = Color.yellow;
    }
    void LightOff()
    {
        transform.GetComponent<MeshRenderer>().material.color = Color.grey;
    }
}
