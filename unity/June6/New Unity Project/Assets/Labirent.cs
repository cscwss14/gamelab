using UnityEngine;
using System.Collections;
using System.Linq;


public class Labirent : MonoBehaviour {

    public bool[,] CoinArray;
    public Transform[] BlinkBeginArray = new Transform[2];
    public ArrayList RandomBlink = new ArrayList();
    public Transform[,] LedArray;
    private Vector2 _patternSize;
    public Pattern ChoosenPattern = 0;
    public int PatternCount=0;
    public Transform currentLed;
    public Transform currentLedghost;
    public string direction;
    public string directionghost;
    public bool gameOver = false;
    public int Score = 0;
    public Color color;
    public Color Scoreboard;
    public bool isPlaying;
    public float PacSpeed = 0.2f;
    public int pause = 1;
    public float BlinkTime = 5f;
    public bool Without = false;
 public enum Pattern : byte
    {
        Yibin = 0,
        Sunny = 1,
        Eliza = 2,
        Sahar = 3,
        Sunny2 = 4,
        Score = 5,
       
    }
 public void InitializeCoins()
    {
        GenerateArray(ChoosenPattern);
        LedArray = new Transform[(int)_patternSize.y, (int)_patternSize.x];
        direction = "Right";
        directionghost = "Left";
        for (int i = 0; i < (_patternSize.x-1*_patternSize.y-1); i++)
        {
            var coin = Instantiate(Resources.Load("LED"), new Vector3(), Quaternion.identity) as GameObject;

            if (coin != null)
            {
                coin.gameObject.active = false;
               // coin.gameObject.transform.parent = ItemManager.Current.Level;

                
            }
        }
        
    }
 public void Pause()
 { 
 
 if(pause == -1){
     StopCoroutine("GhostWalk");
     StopCoroutine("GenerateWalk");
     LedArray[21, 0].GetComponent<Node>().StopAllCoroutines();
     LedArray[21, 25].GetComponent<Node>().StopAllCoroutines();
     LedArray[3, 25].GetComponent<Node>().StopAllCoroutines();
     LedArray[3, 0].GetComponent<Node>().StopAllCoroutines();
 }
 else if (pause == 1) {
     StartCoroutine("GhostWalk");
     StartCoroutine("GenerateWalk");
     LedArray[21, 0].GetComponent<Node>().BlinkBoost();
     LedArray[21, 25].GetComponent<Node>().BlinkBoost();
     LedArray[3, 25].GetComponent<Node>().BlinkBoost();
     LedArray[3, 0].GetComponent<Node>().BlinkBoost();
 }
 
 
 
 }
    public Transform GetCoin()
    {
        
        
            var coin = Instantiate(Resources.Load("LED"), new Vector3(), Quaternion.identity) as GameObject;
            coin.GetComponent<Node>().Initiator = this.transform;
            coin.GetComponent<GhostNode>().Initiator = this.transform;
            if (coin != null)
            {
                // coin.transform.parent = ItemManager.Current.Level;

                return coin.transform;
            }
            else return null;
    }
    public Transform GetWall()
    {


        var wall = Instantiate(Resources.Load("Wall"), new Vector3(), Quaternion.identity) as GameObject;
        
        if (wall != null)
        {
            // coin.transform.parent = ItemManager.Current.Level;

            return wall.transform;
        }
        else return null;
    }

    private void CreateCoins()
    {
        
            DrawCoins(ChoosenPattern, new Vector3(-200, -200,  0f ), 2);
        
    }

    public void DrawCoins(Pattern pattern, Vector3 startingPoint, float offset)
    {
        //GenerateArray(pattern);

        for (int i = 0; i < _patternSize.y; i++)
        {
            for (int j = 0; j < _patternSize.x; j++)
            {
                if (CoinArray[i, j])
                {
                    Vector3 targetPosition = new Vector3(startingPoint.y + (40 * j + offset), startingPoint.x + (40 * i - offset), startingPoint.z);

                    Transform currentCoin = GetCoin();

                    currentCoin.transform.position = targetPosition;
                    currentCoin.gameObject.active = true;
                    //if(CoinArray[j+1, i] != null)
                    //{
                    //    currentCoin.gameObject.GetComponent<Node>().transform.right = 
                    //}
                    LedArray[i,j] = currentCoin;

                    if (PatternCount == 0) 
                    {
                        currentLed = currentCoin.gameObject.transform;
                    }

                    PatternCount++;

                }
                else
                {
                    Vector3 targetPosition = new Vector3(startingPoint.y + (40 * j + offset), startingPoint.x + (40 * i - offset), startingPoint.z);

                    Transform currentWall = GetWall();
                    LedArray[i, j] = null;
                    currentWall.transform.position = targetPosition;
                    currentWall.gameObject.active = false;
                }

            }
        }
    }

    public void AssignNeighbors()
    {
        int Id = 0;

        for (int j = 0; j < _patternSize.y; j++)
        {
            for (int i = 0; i < _patternSize.x; i++)
            {

                if (LedArray[j, i] != null)
                {
                    LedArray[j, i].GetComponent<Node>().x = j;
                    LedArray[j, i].GetComponent<Node>().y = i;
                    if (j + 1 < _patternSize.y && LedArray[j + 1, i] != null)
                    {
                        LedArray[j, i].GetComponent<Node>().Up = LedArray[j + 1, i];
                        LedArray[j, i].GetComponent<GhostNode>().Up = LedArray[j + 1, i]; 
                    }
                    if (j >=1  && LedArray[j - 1, i] != null)
                    {
                        LedArray[j, i].GetComponent<Node>().Down = LedArray[j - 1, i];
                        LedArray[j, i].GetComponent<GhostNode>().Down = LedArray[j - 1, i];
                    }
                    if (i >= 1 && LedArray[j, i-1] != null)
                    {
                        LedArray[j, i].GetComponent<Node>().Left = LedArray[j , i-1];
                        LedArray[j, i].GetComponent<GhostNode>().Left = LedArray[j, i - 1];
                    }
                    if (i+1 < _patternSize.x && LedArray[j, i + 1] != null)
                    {
                        LedArray[j, i].GetComponent<Node>().Right = LedArray[j, i + 1];
                        LedArray[j, i].GetComponent<GhostNode>().Right = LedArray[j, i + 1];
                    }

                    LedArray[j, i].GetComponent<Node>().Id = Id;
                    LedArray[j, i].GetComponent<GhostNode>().Id = Id;
                    Id++;
                }



            }
        }

        currentLed = LedArray[0, 0];
        currentLedghost = LedArray[12, 25];

         

    }


 public void GenerateArray(Pattern pattern)
    {
        #region Patterns
        switch (pattern)
        {
               
                              

            


            case Pattern.Sunny2:
                CoinArray = new[,] { { true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	true,	false,	false,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,},
                                     { true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	true,	true,	true,	true,	true,	false,	false,	false,	true,	false,	false,	false,	true,},
                                     { false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	true,	true,	true,	true,},
                                     { false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,},
                                     { false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	true,	true,	true,	true,	false,	false,	false,	true,},
                                     { false,	false,	true,	false,	false,	false,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	true,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	true,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	true,	true,	true,	false,	false,	false,	false,	false,	true,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	true,	false,	false,	false,	false,	false,	true,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	true,	true,	true,	false,	false,	false,	false,	false,	true,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	true,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	true,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { false,	false,	true,	false,	false,	false,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	true,	true,	true,	true,	false,	false,	false,	true,},
                                     { false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,},
                                     { false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	true,	true,	true,	true,},
                                     { true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	true,	true,	true,	true,	true,	false,	false,	false,	true,	false,	false,	false,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,},
                                     { true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	true,	false,	false,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,},
                                     };
                _patternSize.x = 38;
                _patternSize.y = 27;
                break;
            case Pattern.Eliza:
                CoinArray = new[,] { { true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	true,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	true,	false,	true,	false,	false,	false,	false,	false,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	true,	true,	true,	true,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	true,	false,	true,	true,	true,	true,	true,	true,},
                                     { false,	false,	false,	false,	false,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	true,	false,	true,	false,	false,	false,	false,	false,},
                                     { true,	true,	true,	true,	true,	true,	false,	true,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	true,	true,	true,	true,	true,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	true,	false,	true,	false,	true,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	true,},
                                     { true,	true,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	true,	false,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	true,},
                                     { true,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	true,	true,	true,	false,	false,	false,	false,	false,	true,	false,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,},
                                     { false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	true,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	true,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	true,	true,	true,	false,	false,	false,	false,	false,	true,	false,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	true,},
                                     { true,	true,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	true,	false,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	true,},
                                     { true,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	true,	false,	true,	false,	true,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	true,	true,	true,	true,	true,	false,	true,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	true,	true,	true,	true,	true,	true,},
                                     { false,	false,	false,	false,	false,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	true,	false,	true,	false,	false,	false,	false,	false,},
                                     { true,	true,	true,	true,	true,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	true,	false,	true,	true,	true,	true,	true,	true,},
                                     { true,	false,	false,	false,	false,	false,	false,	true,	false,	true,	false,	false,	false,	false,	false,	true,	false,	true,	false,	true,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	true,},
                                     { true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	true,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,},
                                     };
                _patternSize.x = 33;
                _patternSize.y = 26;
                break;
            case Pattern.Sunny:
               
                CoinArray = new[,] { {false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false, },
                                     {false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	true,	false,	false,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false, },
                                     {false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false, },
                                     {false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false, },
                                     {false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false, },
                                     {false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	true,	true,	true,	true,	true,	false,	false,	false,	true,	false, },
                                     {false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false, },
                                     {false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	false,	true,	true,	true,	true,	true,	false, },
                                     {false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false, },
                                     {false,	true,	true,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false, },
                                     {false,	true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false, },
                                     {false,	true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false, },
                                     {false,	true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false, },
                                     {false,	true,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false, },
                                     {false,	true,	true,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false, },
                                     {false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false, },
                                     {false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false, },
                                     {false,	false,	false,	true,	false,	false,	false,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	false,	true,	true,	true,	true,	true,	false, },
                                     {false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false, },
                                     {false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false, },
                                     {false,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	true,	true,	true,	true,	true,	false,	false,	false,	true,	false, },
                                     {false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false, },
                                     {false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false, },
                                     {false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false, },
                                     {false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	true,	false,	false,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false, },
                                     {false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	true,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false,	false, },
                                     };
                _patternSize.x = 36;
                _patternSize.y = 26;
                break;
            case Pattern.Yibin: 
                CoinArray = new[,] { { true, true,  true,  true,   true,  true,  true,  true,  true,  true,  true,  true,  true,  true,  true,  true,  true , true, true,  true,  true,  true,  true,  true,  true,  true   },
                                     { true, false, false, false,  false, false, false, false, true,  false, false, false, false, false, false, false, false, true, false, false, false, false, false, false, false, true   },
                                     { true, false, false, false,  false, false, false, false, true,  false, false, false, false, false, false, false, false, true, false, false, false, false, false, false, false, true   },
                                     { true, true,  true,  true,   true,  true,  true,  true,  true,  false, false, true,  true,  true,  true,  false, false, true, true,  true,  true,  true,  true,  true,  true,  true   },
                                     { true, false, false, false,  false, false, false, false, true,  false, false, true,  false, false, true,  false, false, true, false, false, false, false, false, false, false, true   },
                                     { true, false, false, false,  false, false, false, false, true,  false, false, true,  false, false, true,  false, false, true, false, false, false, false, false, false, false, true   },
                                     { true, false, false, true,   true,  true,  true,  true,  true,  true,  true,  true,  false, false, true,  true,  true,  true, true,  true,  true,  true,  true,  false, false, true   },
                                     { true, false, false, true,   false, false, false, false, true,  false, false, false, false, false, false, false, false, true, false, false, false, false, true,  false, false, true   },
                                     { true, false, false, true,   false, false, false, false, true,  false, false, false, false, false, false, false, false, true, false, false, false, false, true,  false, false, true   },
                                     { true, true,  true,  true,   true,  true,  false, false, true,  true,  true,  true,  true,  true,  true,  true,  true , true, false, false, true,  true,  true,  true,  true,  true   },
                                     { false,false, false, false,  false, true,  false, false, true,  false, false, false, false, false, false, false, false, true, false, false, true, false, false, false, false,  false  },
                                     { false,false, false, false,  false, true,  false, false, true,  false, false, false, false, false, false, false, false, true, false, false, true, false, false, false, false,  false  },
                                     { true, true,  true,  true,   true,  true,  true,  true,  true,  false, false, false, false, false, false, false, false, true, true,  true,  true,  true,  true,  true,  true,  true   },
                                     { false,false, false, false,  false, true,  false, false, true,  false, false, false, false, false, false, false, false, true, false, false, true, false, false, false, false,  false  },
                                     { false,false, false, false,  false, true,  false, false, true,  false, false, false, false, false, false, false, false, true, false, false, true, false, false, false, false,  false  },
                                     { true, true,  true,  true,   true,  true,  false, false, true,  true,  true,  true,  true,  true,  true,  true,  true , true, false, false, true,  true,  true,  true,  true,  true   },
                                     { true, false, true,  false,  false, false, false, false, false, false, false, true,  false, false, true,  false, false, false,false, false, false, false, false, true, false,  true   },
                                     { true, false, true,  false,  false, false, false, false, false, false, false, true,  false, false, true,  false, false, false,false, false, false, false, false, true, false,  true   },
                                     { true, false, true,  true,   true,  true,  true,  true,  true,  true,  true,  true,  false, false, true,  true,  true,  true, true,  true,  true,  true,  true,  true, false,  true   },
                                     { true, false, true,  false,  false, false, false, false, true,  false, false, false, false, false, false, false, false, true, false, false, false, false, false, true, false,  true   },
                                     { true, false, true,  false,  false, false, false, false, true,  false, false, false, false, false, false, false, false, true, false, false, false, false, false, true, false,  true   },
                                     { true, true,  true,  true,   true,  true,  true,  true,  true,  true,  true,  true,  true,  true,  true,  true,  true , true, true,  true,  true,  true,  true,  true, true,   true   },
                                     { true, false, false, false, false,  true, false,  false, false, false, false, true,  false, false, true,  false, false, false,false, false, true,  false, false, false,false,  true   },
                                     { true, false, false, false, false,  true, false,  false, false, false, false, true,  false, false, true,  false, false, false,false, false, true,  false, false, false,false,  true   },
                                     { true, false, false, false, false,  true, false,  false, true,  true,  true,  true,  false, false, true,  true,  true,  true, false, false, true,  false, false, false,false,  true   },
                                     { true, false, false, false, false,  true, false,  false, true,  false, false, false, false, false, false, false, false, true, false, false, true,  false, false, false,false,  true   },
                                     { true, false, false, false, false,  true, false,  false, true,  false, false, false, false, false, false, false, false, true, false, false, true,  false, false, false,false,  true   },
                                     { true, true,  true,  true,   true,  true,  true,  true,  true,  true,  true,  true,  true,  true,  true,  true,  true , true, true,  true,  true,  true,  true,  true, true,   true   },
                                     };
                
                _patternSize.x = 26;
                _patternSize.y = 28;
                break;

           

            case Pattern.Sahar:
                CoinArray = new[,] { {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	true,	true,	true,	true,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	true,	true,	true,	true,	true,	false,	false,	false,	false,	true,	true,	true,	true,	true,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,	true,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                     {false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,	false,	true,	false,	false,	false,},
                                   
                                     };

                _patternSize.x = 30;
                _patternSize.y = 30;
                break;
            case Pattern.Score:
                CoinArray = new[,] {  { true,	true,	true,	false, true,	true,	true,	false,  	false,	false,  false,	false,  true,	true,	true,	false,false,	true,	false,},
                                      { true,	false,	true,	false, false,	false,  true,	false,  	false,	true,   false,	false,  true,	false,	true,	false,false,	true,	false,},
                                      { true,	false,	true,	false, true,	true,	true,	false,  	false,	false,  false,	false,  true,	false,	true,	false,false,	true,	false,},
                                      { true,	false,	true,	false, true,	false,	false,	false,  	false,	true,   false,	false,  true,	false,	true,	false,false,	true,	false,},
                                      { true,	true,	true,	false, true,	true,	true,	false,  	false,	false,  false,	false,  true,	true,	true,	false,false,	true,	false,}};



                _patternSize.x = 18;
                _patternSize.y = 5;
                break;
        }
        #endregion
    }

 


	// Use this for initialization
	void Start () {
        //Converter.Instance.ReadExcel();
        InitializeCoins();
        CreateCoins();
        if (ChoosenPattern != Pattern.Score)
        {
            AssignNeighbors();
            StartCoroutine(BeginForBlink());
          
           
        }
        else
        {

            for (int j = 0; j < _patternSize.y; j++)
            {
                for (int i = 0; i < _patternSize.x; i++)
                {

                    if (LedArray[j, i] != null)
                    {
                        if(i<8)
                             LedArray[j, i] .GetComponent<MeshRenderer>().material.color = Color.yellow;
                        else if(i>9)
                            LedArray[j, i].GetComponent<MeshRenderer>().material.color = Color.red;
                    }
                }
            }
        
        }
        
	}
	
	// Update is called once per frame
	void Update () {
        isPlaying = GetComponent<AudioSource>().isPlaying;
        if (ChoosenPattern != Pattern.Score)
        {
            if (currentLedghost.GetComponent<GhostNode>().Id == currentLed.GetComponent<Node>().Id && gameOver == false)
            {
                gameOver = true;
                color = Color.red;
                LedArray[21, 0].GetComponent<Node>().StopAllCoroutines();
                LedArray[21, 25].GetComponent<Node>().StopAllCoroutines();
                LedArray[3, 25].GetComponent<Node>().StopAllCoroutines();
                LedArray[3, 0].GetComponent<Node>().StopAllCoroutines();
                StopAllCoroutines();
                StartCoroutine("SetAll");
            }
        }

	}
    public void Stop()
    {
        Without = true;
        gameOver = true;
        color = Color.grey;
        LedArray[21, 0].GetComponent<Node>().StopAllCoroutines();
        LedArray[21, 25].GetComponent<Node>().StopAllCoroutines();
        LedArray[3, 25].GetComponent<Node>().StopAllCoroutines();
        LedArray[3, 0].GetComponent<Node>().StopAllCoroutines();
        StopAllCoroutines();
        StartCoroutine("SetAll");
    
    }

  
    public IEnumerator SetAll()
    {
        if (Without == false)
        {
            for (int j = 0; j < _patternSize.y; j++)
            {
                for (int i = 0; i < _patternSize.x; i++)
                {

                    if (LedArray[j, i] != null)
                    {
                        LedArray[j, i].GetComponent<MeshRenderer>().material.color = color;

                        yield return new WaitForSeconds(0.01f);

                    }
                }
            }
            yield return new WaitForSeconds(1f);
        }
        for (int j = 0; j < _patternSize.y; j++)
        {
            for (int i = 0; i < _patternSize.x; i++)
            {

                if (LedArray[j, i] != null)
                {
                    LedArray[j, i].GetComponent<MeshRenderer>().material.color = Color.gray;
                  //  LedArray[j, i].GetComponent<Node>().StopAllCoroutines();
                  //  yield return new WaitForSeconds(0.01f);

                }
            }
        }

        Without = false;
    }
    private IEnumerator GenerateWalk()
    {
     
        if(gameOver == false)
        {

            if (Score != PatternCount)
            {
                yield return new WaitForSeconds(PacSpeed);
                currentLed.GetComponent<MeshRenderer>().material.color = Color.yellow;
                currentLed.GetComponent<Node>().Walk();


             

                StartCoroutine("GenerateWalk");
            }
            else 
            {
                gameOver = true;
                color = Color.yellow;
                StopAllCoroutines();
                StartCoroutine("SetAll");
            }
        }
    }
    public IEnumerator GhostWalk()
    {
        if (gameOver == false)
        {

            if (Score != PatternCount)
            {
                yield return new WaitForSeconds(0.2f);
                currentLedghost.GetComponent<MeshRenderer>().material.color = Color.red;
                currentLedghost.GetComponent<GhostNode>().Walk();
            }
        }
        StartCoroutine("GhostWalk");
    }

    public IEnumerator BlinkBegin()
    {

        Color origin,origin2;
       
            origin = BlinkBeginArray[0].GetComponent<MeshRenderer>().material.color;
            origin2 = BlinkBeginArray[1].GetComponent<MeshRenderer>().material.color;
            BlinkBeginArray[0].GetComponent<MeshRenderer>().material.color = Color.white;
            BlinkBeginArray[1].GetComponent<MeshRenderer>().material.color = Color.white;

        yield return new WaitForSeconds(0.5f);
        BlinkBeginArray[0].GetComponent<MeshRenderer>().material.color = origin;
        BlinkBeginArray[1].GetComponent<MeshRenderer>().material.color = origin2;

        yield return new WaitForSeconds(0.5f);
        
        StartCoroutine("BlinkBegin");
    }

    public IEnumerator BeginForBlink()
    {

        yield return new WaitForSeconds(2f);
        currentLed = LedArray[0, 0];
        currentLedghost = LedArray[12, 25];
        BlinkBeginArray[0] = LedArray[0, 0];
        BlinkBeginArray[1] = LedArray[12, 25];
        BlinkBeginArray[0].GetComponent<MeshRenderer>().material.color = Color.yellow;
        BlinkBeginArray[1].GetComponent<MeshRenderer>().material.color = Color.red;

        LedArray[12, 0].GetComponent<Node>().Left = LedArray[12, 25];
        LedArray[12, 25].GetComponent<Node>().Right = LedArray[12, 0];
        StartCoroutine("BlinkBegin");
        yield return new WaitForSeconds(BlinkTime);
        StopCoroutine("BlinkBegin");


        LedArray[21, 0].GetComponent<Node>().isSpecial = true;
        LedArray[21, 25].GetComponent<Node>().isSpecial = true;
        LedArray[3, 25].GetComponent<Node>().isSpecial = true;
        LedArray[3, 0].GetComponent<Node>().isSpecial = true;

        LedArray[21, 0].GetComponent<Node>().BlinkBoost();
        LedArray[21, 25].GetComponent<Node>().BlinkBoost();
        LedArray[3, 25].GetComponent<Node>().BlinkBoost();
        LedArray[3, 0].GetComponent<Node>().BlinkBoost();


        StartCoroutine("GenerateWalk");
        StartCoroutine("GhostWalk");
    
    
    }


    public void Reset()
    {
        Score = 0;
        StopAllCoroutines();
        LedArray[21, 0].GetComponent<Node>().StopAllCoroutines();
        LedArray[21, 25].GetComponent<Node>().StopAllCoroutines();
        LedArray[3, 25].GetComponent<Node>().StopAllCoroutines();
        LedArray[3, 0].GetComponent<Node>().StopAllCoroutines();
        for (int j = 0; j < _patternSize.y; j++)
        {
            for (int i = 0; i < _patternSize.x; i++)
            {

                if (LedArray[j, i] != null)
                {
                    LedArray[j, i].GetComponent<MeshRenderer>().material.color = Color.white;

                    
                }
            }
        }

        
        StartCoroutine("BeginForBlink");
    
    
    }

   //public IEnumerator RandomBlink()
   //{

   //    LedArray[15, Random.Range(8,17)].GetComponent<Node>().BlinkBoost();
   //    LedArray[15, Random.Range(8, 17)].GetComponent<Node>().BlinkBoost();
   
   //    LedArray[9, Random.Range(8, 17)].GetComponent<Node>().BlinkBoost();
   //    LedArray[9, Random.Range(8, 17)].GetComponent<Node>().BlinkBoost();
   
   //    LedArray[21, 2].GetComponent<Node>().BlinkBoost();
   //    LedArray[21, 23].GetComponent<Node>().BlinkBoost();
   
   
   //}
   
}
