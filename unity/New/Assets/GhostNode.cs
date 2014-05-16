using UnityEngine;
using System.Collections;

public class GhostNode : MonoBehaviour
{

    public Transform Led;
    public Transform Left;
    public Transform Right;
    public Transform Up;
    public Transform Down;
    public Transform Initiator;
    public Color PreColor;
    public int Id;
    // Use this for initialization
    void Start()
    {
        PreColor = Color.green;
        // LightOn();
    }

    // Update is called once per frame
    void Update()
    {



    }

    public void Walk()
    {

        if (Initiator.GetComponent<Labirent>().directionghost == "Up")
        {
            if (Up != null)
            {
                LightOff();
                Up.GetComponent<GhostNode>().LightOn();
                Initiator.GetComponent<Labirent>().currentLedghost = Up;
            }
            else
            {
                Initiator.GetComponent<Labirent>().directionghost = Initiator.GetComponent<Keyboard>().ghostPrevious;
            }
        }
        else if (Initiator.GetComponent<Labirent>().directionghost == "Down" && Down != null)
        {
            if (Down != null)
            {
                LightOff();
                Down.GetComponent<GhostNode>().LightOn();
                Initiator.GetComponent<Labirent>().currentLedghost = Down;
            }
            else
            {
                Initiator.GetComponent<Labirent>().directionghost = Initiator.GetComponent<Keyboard>().ghostPrevious;
            }
        }
        else if (Initiator.GetComponent<Labirent>().directionghost == "Left" && Left != null)
        {
            if (Left != null)
            {
                LightOff();
                Left.GetComponent<GhostNode>().LightOn();
                Initiator.GetComponent<Labirent>().currentLedghost = Left;
            }
            else
            {
                Initiator.GetComponent<Labirent>().directionghost = Initiator.GetComponent<Keyboard>().ghostPrevious;
            }

        }
        else if (Initiator.GetComponent<Labirent>().directionghost == "Right" && Right != null)
        {
            if (Right != null)
            {
                LightOff();
                Right.GetComponent<GhostNode>().LightOn();
                Initiator.GetComponent<Labirent>().currentLedghost = Right;
            }
            else
            {
                Initiator.GetComponent<Labirent>().directionghost = Initiator.GetComponent<Keyboard>().ghostPrevious;
            }
        }

    }


    void LightOn()
    {
        PreColor = transform.GetComponent<MeshRenderer>().material.color; 
        transform.GetComponent<MeshRenderer>().material.color = Color.red;
    }
    void LightOff()
    {
        if (transform.GetComponent<MeshRenderer>().material.color != Color.grey)
        {
            transform.GetComponent<MeshRenderer>().material.color = PreColor;
           // transform.GetComponent<MeshRenderer>().material.color = Color.green;
        }

    }
}
