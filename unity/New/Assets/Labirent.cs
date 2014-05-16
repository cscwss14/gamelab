using UnityEngine;
using System.Collections;
using System.Linq;


public class Labirent : MonoBehaviour {

    public bool[,] CoinArray;

    public Transform[,] LedArray;
    private Vector2 _patternSize;
    public Pattern ChoosenPattern = 0;
    public int PatternCount=0;
    public Transform currentLed;
    public Transform currentLedghost;
    public string direction;
    public string directionghost;

 public enum Pattern : byte
    {
        Yibin = 0,
        Sunny = 1,
        Eliza = 2,
        Sahar = 3,
        Sunny2 = 4,
       
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
        currentLedghost = LedArray[0,22];
    
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
        }
        #endregion
    }




	// Use this for initialization
	void Start () {
        InitializeCoins();
        CreateCoins();
        AssignNeighbors();
        StartCoroutine(GenerateWalk());
	}
	
	// Update is called once per frame
	void Update () {

        if (currentLedghost.GetComponent<GhostNode>().Id == currentLed.GetComponent<Node>().Id)
        {
            //SetAll();
        }

	}

    //public IEnumerator SetAll()
    //{

    //    for (int j = 0; j < _patternSize.y; j++)
    //    {
    //        for (int i = 0; i < _patternSize.x; i++)
    //        {

    //            if (LedArray[j, i] != null)
    //            {
    //             //   LedArray[j, i].GetComponent<MeshRenderer>().material.color = color;
    //            }
    //        }
    //    }
    
    
    //}
    private IEnumerator GenerateWalk()
    {
        //Debug.Log("GENERATE BARRIERS COROUTINE");

        yield return new WaitForSeconds(0.7f);
        currentLed.GetComponent<MeshRenderer>().material.color = Color.yellow;
        currentLed.GetComponent<Node>().Walk();


        currentLedghost.GetComponent<MeshRenderer>().material.color = Color.red;
        currentLedghost.GetComponent<GhostNode>().Walk();

        StartCoroutine(GenerateWalk());

    }
}
