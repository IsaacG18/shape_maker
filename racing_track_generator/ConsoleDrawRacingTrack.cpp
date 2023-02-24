/*
Author
~~~~~~
Twitter: @javidx9
Blog: http://www.onelonecoder.com
Discord: https://discord.gg/WhwHUMV

Video:
~~~~~~
https://youtu.be/FlieT66N9OM
*/

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <math.h>
#include <cmath>
#include <stdio.h>
using namespace std;

#define OLC_PGE_APPLICATION

struct sPoint2D
{
	float x;
	float y;
	float length;
};

struct sSpline
{
	vector<sPoint2D> points;
	float fTotalSplineLength = 0.0f;
	bool bIsLooped = true;

	void ReadFile(){
		std::ifstream file("xy_coordinates.txt");
    	std::string line;

		std::getline(file, line);

		while (std::getline(file, line)) {
			float x, y;
			std::sscanf(line.c_str(), "%f,%f", &x, &y);
			sPoint2D point = { x, y, std::sqrt(x * x + y * y) };
			points.push_back(point);
    	}
	}
	void AddPoints(vector<sPoint2D> temp){
		points = temp;
	}

	sPoint2D GetSplinePoint(float t)
	{
		int p0, p1, p2, p3;
		if (!bIsLooped)
		{
			p1 = (int)t + 1;
			p2 = p1 + 1;
			p3 = p2 + 1;
			p0 = p1 - 1;
		}
		else
		{
			p1 = ((int)t) % points.size();
			p2 = (p1 + 1) % points.size();
			p3 = (p2 + 1) % points.size();
			p0 = p1 >= 1 ? p1 - 1 : points.size() - 1;
		}

		t = t - (int)t;

		float tt = t * t;
		float ttt = tt * t;

		float q1 = -ttt + 2.0f * tt - t;
		float q2 = 3.0f * ttt - 5.0f * tt + 2.0f;
		float q3 = -3.0f * ttt + 4.0f * tt + t;
		float q4 = ttt - tt;

		float tx = 0.5f * (points[p0].x * q1 + points[p1].x * q2 + points[p2].x * q3 + points[p3].x * q4);
		float ty = 0.5f * (points[p0].y * q1 + points[p1].y * q2 + points[p2].y * q3 + points[p3].y * q4);

		return{ tx, ty };
	}

	sPoint2D GetSplineGradient(float t)
	{
		int p0, p1, p2, p3;
		if (!bIsLooped)
		{
			p1 = (int)t + 1;
			p2 = p1 + 1;
			p3 = p2 + 1;
			p0 = p1 - 1;
		}
		else
		{
			p1 = ((int)t) % points.size();
			p2 = (p1 + 1) % points.size();
			p3 = (p2 + 1) % points.size();
			p0 = p1 >= 1 ? p1 - 1 : points.size() - 1;
		}

		t = t - (int)t;

		float tt = t * t;
		float ttt = tt * t;

		float q1 = -3.0f * tt + 4.0f * t - 1.0f;
		float q2 = 9.0f * tt - 10.0f * t;
		float q3 = -9.0f * tt + 8.0f * t + 1.0f;
		float q4 = 3.0f * tt - 2.0f * t;

		float tx = 0.5f * (points[p0].x * q1 + points[p1].x * q2 + points[p2].x * q3 + points[p3].x * q4);
		float ty = 0.5f * (points[p0].y * q1 + points[p1].y * q2 + points[p2].y * q3 + points[p3].y * q4);

		return{ tx, ty };
	}

	float CalculateSegmentLength(int node)
	{
		float fLength = 0.0f;
		float fStepSize = 0.1;

		sPoint2D old_point, new_point;
		old_point = GetSplinePoint((float)node);

		for (float t = 0; t < 1.0f; t += fStepSize) 
		{
			new_point = GetSplinePoint((float)node + t);
			fLength += sqrtf((new_point.x - old_point.x) * (new_point.x - old_point.x)
				+ (new_point.y - old_point.y) * (new_point.y - old_point.y));
			old_point = new_point;
		}

		return fLength;
	}


	float GetNormalisedOffset(float p)
	{
		// Which node is the base?
		int i = 0;
		while (p > points[i].length)
		{
			p -= points[i].length;
			i++;
		}

		// The fractional is the offset 
		return (float)i + (p / points[i].length);
	}


	void UpdateSplineProperties()
	{
		// Use to cache local spline lengths and overall spline length
		fTotalSplineLength = 0.0f;

		if (bIsLooped)
		{
			// Each node has a succeeding length
			for (int i = 0; i < points.size(); i++)
			{
				points[i].length = CalculateSegmentLength(i);
				fTotalSplineLength += points[i].length;
			}
		}
		else
		{
			for (int i = 1; i < points.size() - 2; i++)
			{
				points[i].length = CalculateSegmentLength(i);
				fTotalSplineLength += points[i].length;
			}
		}
	}

	

	// void DrawSelf(olc::PixelGameEngine* gfx, float ox, float oy, float distance, olc::Pixel p = olc::WHITE)
	// {
	// 	if (bIsLooped)
	// 	{
	// 		for (float t = 0; t < (float)points.size() - 0; t += distance)
	// 		{
	// 			sPoint2D pos = GetSplinePoint(t);
	// 			gfx->Draw(pos.x, pos.y, p);
	// 		}
	// 	}
	// 	else // Not Looped
	// 	{
	// 		for (float t = 0; t < (float)points.size() - 3; t += distance)
	// 		{
	// 			sPoint2D pos = GetSplinePoint(t);
	// 			gfx->Draw(pos.x, pos.y, p);
	// 		}
	// 	}
	// }

	

};

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

class RacingTrack
{
public:
	RacingTrack()
	{
		path.ReadFile();
		DealWithPoints();
	}
	RacingTrack(vector<sPoint2D> points)
	{
		path.AddPoints(points);
		DealWithPoints();
	}

private:
	sSpline path, trackInside, trackOutside, racingLine;	// Various splines

	int nNodes = 15;	        // Number of red (controlable) nodes in spline
	float nNodesSpline = 60.0f; // Number of total points in a spline

	float fDisplacement[15]; // Displacement along spline node normal

	int nIterations = 1;
	float fMarker = 1.0f;
	int nSelectedNode = -1;
	int fTrackWidth = 3;

	// Getter methods to access path, boundaries and number of points in a spline in main()
public:
	sSpline getPath()
	{
		return path;
	}
	sSpline getTrackInside()
	{
		return trackInside;
	}
	sSpline getTrackOutside()
	{
		return trackOutside;
	}
	float getNodesSpline()
	{
		return nNodesSpline;
	}
	void DealWithPoints(){
		for (int i = 0; i < path.points.size(); i++)
		{
			sPoint2D point;
			point.x = 0.0f;
			point.y = 0.0f;
			trackInside.points.push_back(point);
			trackOutside.points.push_back(point);


			sPoint2D p1 = path.GetSplinePoint(i);
			sPoint2D g1 = path.GetSplineGradient(i);
			float glen = sqrtf(g1.x * g1.x + g1.y * g1.y);

			trackInside.points[i].x = p1.x + fTrackWidth * (-g1.y / glen);
			trackInside.points[i].y = p1.y + fTrackWidth * (g1.x / glen);
			trackOutside.points[i].x = p1.x - fTrackWidth * (-g1.y / glen);
			trackOutside.points[i].y = p1.y - fTrackWidth * (g1.x / glen);
		}
		
	}

};

extern "C" void my_c_function(double** arr, int rows, int cols, int i) {
	std::vector<sPoint2D> vec;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            sPoint2D point;
            point.x = static_cast<float>(arr[i][j]);
            point.y = static_cast<float>(arr[i][j + 1]);
            point.length = static_cast<float>(arr[i][j + 2]);
            vec.push_back(point);
            j += 2;
        }
    }
	RacingTrack demo(vec);

	sSpline path = demo.getPath();
	sSpline trackInside = demo.getTrackInside();
	sSpline trackOutside = demo.getTrackOutside();
	float nNodesSpline = demo.getNodesSpline();
	float distance = (float)path.points.size() / nNodesSpline;

	std::string filename = "data/data_" + std::to_string(i) + ".csv";
	std::ofstream fout(filename);

	fout << "xPath" << "," << "yPath" << "," << "xOutside" << "," << "yOutside" << "," << "xInside" << "," << "yInside" << endl;
	for (float i = (float)path.points.size(); i > 0; i -= distance)
	{
		sPoint2D p = path.GetSplinePoint(i);
		sPoint2D inside = trackInside.GetSplinePoint(i);
		sPoint2D outside = trackOutside.GetSplinePoint(i);
		fout << p.x << "," << p.y << "," << inside.x << "," << inside.y << "," << outside.x << "," << outside.y << endl;
	}

	fout.close();
}

// int main()
// {
// 	RacingTrack demo;
	

// 	sSpline path = demo.getPath();
// 	sSpline trackInside = demo.getTrackInside();
// 	sSpline trackOutside = demo.getTrackOutside();
// 	float nNodesSpline = demo.getNodesSpline();
// 	float distance = (float)path.points.size() / nNodesSpline;

// 	ofstream fout("data/data.csv");

// 	fout << "xPath" << "," << "yPath" << "," << "xOutside" << "," << "yOutside" << "," << "xInside" << "," << "yInside" << endl;
// 	for (float i = (float)path.points.size(); i > 0; i -= distance)
// 	{
// 		sPoint2D p = path.GetSplinePoint(i);
// 		sPoint2D inside = trackInside.GetSplinePoint(i);
// 		sPoint2D outside = trackOutside.GetSplinePoint(i);
// 		fout << p.x << "," << p.y << "," << inside.x << "," << inside.y << "," << outside.x << "," << outside.y << endl;
// 	}

// 	fout.close();

// 	return 0;
// }
