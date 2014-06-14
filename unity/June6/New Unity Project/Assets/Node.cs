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
    public bool Eaten = false;
    public int x;
    public int y;
    public AudioSource hurp;
    public bool isSpecial;
    public float WaitingBoostTime = 6f;
	// Use this for initialization
	void Start () {
       // LightOn();
        hurp = Initiator.GetComponent<AudioSource>();
       // if(isSpecial == true)
       
	}
	
	// Update is called once per frame
	void Update () {


       
	}
    public void BlinkBoost()
    {

        StartCoroutine("BlinkBoosts");
    
    }
     public IEnumerator SpeedBoost() {

         Initiator.GetComponent<Labirent>().PacSpeed /= 2;
         yield return new WaitForSeconds(WaitingBoostTime);
         Initiator.GetComponent<Labirent>().PacSpeed *= 2;
    
    }


    public IEnumerator BlinkBoosts()
    {
        
        transform.GetComponent<MeshRenderer>().material.color = Color.green;
       
        yield return new WaitForSeconds(0.5f);
        transform.GetComponent<MeshRenderer>().material.color = Color.white;
      
        yield return new WaitForSeconds(0.5f);
        StartCoroutine("BlinkBoosts");
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
        if (Eaten == false)
        {
            Initiator.GetComponent<Labirent>().Score++;
        }

        Eaten = true;
        
        transform.GetComponent<MeshRenderer>().material.color = Color.cyan;

        if (isSpecial)
        {

            StopCoroutine("BlinkBoosts");
            StartCoroutine("SpeedBoost");
            isSpecial = false;

            
        }




       // if(!hurp.isPlaying)
       // hurp.Play() ;
    }


   
}
