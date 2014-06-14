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
        if (transform.GetComponent<Labirent>().gameOver)
        {
            if (Input.GetKeyDown(KeyCode.B))
            {
                transform.GetComponent<Labirent>().currentLed = transform.GetComponent<Labirent>().LedArray[0, 0];
                transform.GetComponent<Labirent>().currentLedghost = transform.GetComponent<Labirent>().LedArray[12, 25];
                transform.GetComponent<Labirent>().gameOver = false;
                transform.GetComponent<Labirent>().Reset();
            }
        }
        if (transform.GetComponent<Labirent>().pause == 1)
        {
            if (Input.GetKeyDown(KeyCode.P))
            {
                transform.GetComponent<Labirent>().pause = -1;
                transform.GetComponent<Labirent>().Pause();
            }
        }
        if (transform.GetComponent<Labirent>().pause == -1){
            if(Input.GetKeyDown(KeyCode.B))
            {
                transform.GetComponent<Labirent>().pause = 1;
                transform.GetComponent<Labirent>().Pause();
            }
        }
        if (Input.GetKeyDown(KeyCode.R))
        {
            transform.GetComponent<Labirent>().Reset();
           
        }
        if (Input.GetKeyDown(KeyCode.T))
        {
            transform.GetComponent<Labirent>().Stop();
        
        }
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
