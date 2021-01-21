import math


class Quaternion:
    def __init__(self, axis=None, angle=None, position=None, quat=None):
        if axis and angle:
            theta = angle / 2.0
            self.i = [axis[0] * math.sin(theta), axis[1] * math.sin(theta), axis[2] * math.sin(theta)]
            self.r = math.cos(theta)
            self.conj = [self.r, -self.i[0], -self.i[1], -self.i[2]]
        elif position:
            self.r = 0.0
            self.i = [position[0], position[1], position[2]]
        elif quat:
            self.r = quat[0]
            self.i = [quat[1], quat[2], quat[3]]
        else:
            self.i = [0.0, 0.0, 0.0]
            self.r = 0.0
            self.conj = [0.0, 0.0, 0.0, 0.0]

    def rotatePosition(self, pos):
        tmp = self.multiply(pos)

        result = tmp.multiply(Quaternion(quat=self.conj))

        return [result.i[0], result.i[1], result.i[2]]

    def multiply(self, other):
        tmp = Quaternion()
        tmp.r = (self.r * other.r) - (self.i[0] * other.i[0]) - (self.i[1] * other.i[1]) - (self.i[2] * other.i[2])
        tmp.i[0] = (self.r * other.i[0]) + (self.i[0] * other.r) + (self.i[1] * other.i[2]) - (self.i[2] * other.i[1])
        tmp.i[1] = (self.r * other.i[1]) - (self.i[0] * other.i[2]) + (self.i[1] * other.r) + (self.i[2] * other.i[0])
        tmp.i[2] = (self.r * other.i[2]) + (self.i[0] * other.i[1]) - (self.i[1] * other.i[0]) + (self.i[2] * other.r)
        return tmp


def main():
    # Get relevant coordinates from Pdb file
    coordinates = getCoordinatesPdbFile('data/1lyd.pdb')
    rotatedCoordinates = []
    my_axis = [0, 2 / math.sqrt(5), 1 / math.sqrt(5)]
    my_angle = 30.0
    my_angle = math.radians(my_angle)
    my_quat = Quaternion(axis=my_axis, angle=my_angle)

    # Rotate coordinates
    for i in range(len(coordinates)):
        rotated_vector = my_quat.rotatePosition(Quaternion(position=coordinates[i]))
        rotatedCoordinates.append(rotated_vector)

    # Store coordinates back in Pdb file
    setCoordinatesPdbFile('data/1lyd.pdb', 'data/1lyd_rotated.pdb', rotatedCoordinates)


def setCoordinatesPdbFile(file_to_read, file_to_write, rotatedCoordinates):
    with open(file_to_read) as f:
        list_ = list(f)
    i = 0
    with open(file_to_write, 'w') as output:
        for line in list_:
            id_ = line.split()[0]
            if id_ == 'ATOM' or id_ == 'HETATM':
                output.write("{:6s}{:5s} {:^4s}{:1s}{:3s} {:1s}{:4s}{:1s}   {:8.3f}{:8.3f}{:8.3f}{:6.2s}{:6.2s}          {:>2s}{:2s}\n".format(
                    line[0:6], line[6:11], line[12:16], line[16:17], line[17:20], line[21:22], line[22:26], line[26:27],
                    rotatedCoordinates[i][0], rotatedCoordinates[i][1], rotatedCoordinates[i][2], line[54:60],
                    line[60:66], line[76:78], line[78:80]))
                i += 1
            else:
                output.write(line)


def getCoordinatesPdbFile(fileName):
    coordinateList = []

    for line in open(fileName):
        line_ = line.split()
        id_ = line_[0]
        if id_ == 'ATOM' or id_ == 'HETATM':
            coordinateList.append([float(line_[6]), float(line_[7]), float(line_[8])])

    return coordinateList


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
