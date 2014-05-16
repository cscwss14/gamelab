using UnityEngine;
using System.Collections;

public class Keyboard : MonoBehaviour {


    public string Previous;

    public string ghostPrevious;
	// Use this for initialization
	void Start () {
        Previous = "Right";
        ghostPrevious = "Left";
	}
	
	// Update is called once per frame
	void Update () {

        if (Input.GetKeyDown("right"))
        {
            if (transform.GetComponent<Labirent>().currentLed.GetComponent<Node>().Right != null)
            {
                Previous = gameObject.GetComponent<Labirent>().direction;
                gameObject.GetComponent<Labirent>().direction = "Right";
            }
        }
        else if (Input.GetKeyDown("left"))
        {
            if (transform.GetComponent<Labirent>().currentLed.GetComponent<Node>().Left != null)
            {
                Previous = gameObject.GetComponent<Labirent>().direction;
                gameObject.GetComponent<Labirent>().direction = "Left";
            }
        }
        else if (Input.GetKeyDown("up"))
        {
            if (transform.GetComponent<Labirent>().currentLed.GetComponent<Node>().Up != null)
            {
                Previous = gameObject.GetComponent<Labirent>().direction;
                gameObject.GetComponent<Labirent>().direction = "Up";
            }
        }
        else if (Input.GetKeyDown("down"))
        {
            if (transform.GetComponent<Labirent>().currentLed.GetComponent<Node>().Down != null)
            {
                Previous = gameObject.GetComponent<Labirent>().direction;
                gameObject.GetComponent<Labirent>().direction = "Down";
            }
        }


        if (Input.GetKeyDown(KeyCode.D))
        {
            if (transform.GetComponent<Labirent>().currentLedghost.GetComponent<Node>().Right != null)
            {
                Previous = gameObject.GetComponent<Labirent>().directionghost;
                gameObject.GetComponent<Labirent>().directionghost = "Right";
            }
        }
        else if (Input.GetKeyDown(KeyCode.A))
        {
            if (transform.GetComponent<Labirent>().currentLedghost.GetComponent<Node>().Left != null)
            {
                Previous = gameObject.GetComponent<Labirent>().directionghost;
                gameObject.GetComponent<Labirent>().directionghost = "Left";
            }
        }
        else if (Input.GetKeyDown(KeyCode.W))
        {
            if (transform.GetComponent<Labirent>().currentLedghost.GetComponent<Node>().Up != null)
            {
                Previous = gameObject.GetComponent<Labirent>().directionghost;
                gameObject.GetComponent<Labirent>().directionghost = "Up";
            }
        }
        else if (Input.GetKeyDown(KeyCode.S))
        {
            if (transform.GetComponent<Labirent>().currentLedghost.GetComponent<Node>().Down != null)
            {
                Previous = gameObject.GetComponent<Labirent>().directionghost;
                gameObject.GetComponent<Labirent>().directionghost = "Down";
            }
        }
	}
}
